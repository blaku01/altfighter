from character.utils import when_mission_ends
from common.models import Stats
from django.db import models
from django.db.models import Q
from django.utils import timezone
from item.models import Item
from numpy import power
from users.models import User


class CharacterManager(models.Manager):
    def get(self, id):
        character = super().get_queryset().get(id=id)
        mission = character.missions.get(~Q(time_started=None))
        if mission.has_finished:
            character.currency += mission.currency
            character.current_exp += mission.exp

            character.level_up_if_possible()

            character.save()
        return character

# Create your models here.
class Character(Stats):
    WARRIOR = 1
    HUNTER = 2
    MAGE = 3

    CHARACTER_CLASSES = (
        (WARRIOR, "warrior"),
        (HUNTER, "hunter"),
        (MAGE, "mage"),
    )
    nickname = models.CharField(null=True, unique=True, max_length=10)
    created_by = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    type = models.PositiveSmallIntegerField(choices=CHARACTER_CLASSES, null=True)
    currency = models.IntegerField(null=True, blank=True, default=0)
    level = models.IntegerField(null=True, blank=True, default=1)
    battle_points = models.IntegerField(null=True, blank=True, default=0)
    current_exp = models.IntegerField(null=True, blank=True, default=0)
    last_attacked_at = models.DateTimeField(null=True, blank=True)
    objects = CharacterManager()

    # might move fight-related things to utils / Fight app
    @property
    def damage(self):
        weapon = Item.objects.filter(
            belongs_to=self, equipped=True, type=Item.ItemType.WEAPON
        ).first()
        if weapon is not None:
            return weapon.damage * (1 + self.strength / 10)
        return 1 + self.strength / 10

    @property
    def health(self):
        return self.vitality * 2 * (self.level + 1)

    def calculate_crit(self, enemy):
        return self.luck * 2.5 / enemy.level

    @property
    def exp_to_next_level(self):
        return power(self.level, 2) - self.current_exp

    @property
    def equipped_items(self):
        items = Item.objects.filter(belongs_to=self, equipped=True)
        return items

    @property
    def backpack(self):
        items = Item.objects.filter(belongs_to=self, equipped=False, purchased=True)
        return items

    @property
    def shop(self):
        items = Item.objects.filter(belongs_to=self, purchased=False)
        return items

    @property
    def total_stats(self):
        strength = self.strength
        agility = self.agility
        vitality = self.vitality
        luck = self.luck
        for item in self.equipped_items:
            strength += item.strength
            agility += item.agility
            vitality += item.vitality
            luck += item.luck
        return {
            "strength": strength,
            "agility": agility,
            "vitality": vitality,
            "luck": luck,
        }

    @property
    def missions(self):
        missions = Mission.objects.filter(belongs_to=self)
        return missions

    @property
    def fight_cooldown(self):
        seconds_since_attack = (
            timezone.now().timestamp() - self.last_attacked_at.timestamp()
        )
        return seconds_since_attack - 10 * 60

    def level_up_if_possible(self):
        while self.exp_to_next_level <= 0:
            self.current_exp = self.exp_to_next_level * -1
            self.level += 1
        return self

    def __str__(self):
        return self.nickname


class Mission(models.Model):
    name = models.CharField(null=True, max_length=30)
    exp = models.IntegerField()
    currency = models.IntegerField()
    time = models.TimeField()
    time_started = models.DateTimeField(blank=True, null=True)
    belongs_to = models.ForeignKey(Character, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def has_started(self):
        if self.time_started is not None:
            return True
        return False

    @property
    def has_finished(self):
        if self.time_started is not None:
            to_mission_end = when_mission_ends(self)
            if to_mission_end <= 0:
                return True
        return False

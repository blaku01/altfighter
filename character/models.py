from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Stats(models.Model):
    class Meta:
        abstract = True
    strength = models.IntegerField(blank=True, null=True)
    agility = models.IntegerField(blank=True, null=True)
    vitality = models.IntegerField(blank=True, null=True)
    luck = models.IntegerField(blank=True, null=True)

    def __add__(self, obj):

        if obj:
            strength = self.strength + obj.strength
            agility = self.agility + obj.agility
            vitality = self.vitality + obj.vitality
            luck = self.luck + obj.luck
            return {'strength':strength, 'agility':agility, 'vitality':vitality, 'luck':luck}
        return self

    
    def __str__(self):
        text = f"{self.strength} {self.agility} {self.vitality} {self.luck}"
        return text

    def calculate_total_stats(self):
        return self.strength + self.agility + self.vitality + self.luck


class Character(Stats):
    nickname = models.CharField(null=True, unique=True, max_length=10)
    created_by = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    currency = models.IntegerField(null=True, blank=True, default=0)
    level = models.IntegerField(null=True,blank=True,  default=1)
    battle_points = models.IntegerField(null=True, blank=True, default = 0)
    current_exp = models.IntegerField(null=True, blank=True, default=1)

    @property
    def exp_to_next_level(self):
        return self.level^3 - self.current_exp

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
        stats = self
        print(self.strength)
        for item in self.equipped_items:
            self += item
        return stats
    
    @property
    def missions(self):
        missions = Mission.objects.filter(belongs_to=self)
        return missions

    def __str__(self):
        return self.nickname

class Item(Stats):
    name = models.CharField(null=True, max_length=10)
    damage = models.IntegerField(blank=True, default=0)
    equipped = models.BooleanField(null=True, blank=True, default=False)
    purchased = models.BooleanField(null=True, blank=True, default=False)
    price = models.IntegerField(null=True)
    belongs_to = models.ForeignKey(Character, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Mission(models.Model):
    name = models.CharField(null=True, max_length = 30)
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

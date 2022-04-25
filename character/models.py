from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Stats(models.Model):
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
            return Stats(strength=strength, agility=agility, vitality=vitality, luck=luck)
        return self

    
    def __str__(self):
        text = f"{self.strength} {self.agility} {self.vitality} {self.luck}"
        return text

    def calculate_total_stats(self):
        return self.strength + self.agility + self.vitality + self.luck


class Character(models.Model):
    nickname = models.CharField(null=True, unique=True, max_length=10)
    created_by = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    currency = models.IntegerField(null=True, blank=True, default=0)
    level = models.IntegerField(null=True,blank=True,  default=1)
    battle_points = models.IntegerField(null=True, blank=True, default = 0)
    current_exp = models.IntegerField(null=True, blank=True, default=1)
    base_stats = models.OneToOneField(Stats,null=True, blank=True, on_delete=models.CASCADE)

    @property
    def exp_to_next_level(self):
        return self.level^3 - self.current_exp

    @property
    def equipped_items(self):
        items = Item.objects.filter(belongs_to=self, equipped=True)
        return items

    @property
    def backpack(self):
        items = Item.objects.filter(belongs_to=self, equipped=False, pucharsed=True)
        return items

    @property
    def shop(self):
        items = Item.objects.filter(belongs_to=self, pucharsed=False)
        return items

    @property
    def total_stats(self):
        stats= self.base_stats
        for i in [item.stats for item in self.equipped_items]:
            stats += i
        return stats
    

    def level_up(self):
        self.level += 1
        self.current_exp = 1

    def __str__(self):
        return self.nickname

class Item(models.Model):
    name = models.CharField(null=True, max_length=10)
    stats = models.OneToOneField(Stats, null=True, blank=True, on_delete=models.CASCADE)
    damage = models.IntegerField(blank=True, default=0)
    equipped = models.BooleanField(null=True, blank=True, default=False)
    pucharsed = models.BooleanField(null=True, blank=True, default=False)
    price = models.IntegerField(null=True)
    belongs_to = models.ForeignKey(Character, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
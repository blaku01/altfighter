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
            return Stats(strength, agility, vitality, luck)
        return self

    
    def __str__(self):
        text = f"{self.strength} {self.agility} {self.vitality} {self.luck}"
        return text

class Item(models.Model):
    name = models.CharField(null=True, max_length=10)
    stats = models.ForeignKey(Stats, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Weapon(Item):
    damage = models.IntegerField(blank=True, default=1)


class Character(models.Model):
    DEFAULT_STATS_ID = 1
    nickname = models.CharField(null=True, max_length=10)
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)    
    level = models.IntegerField(null=True,blank=True,  default=1)
    battle_points = models.IntegerField(null=True, blank=True, default = 0)
    current_exp = models.IntegerField(null=True, blank=True, default=1)
    base_stats = models.ForeignKey(Stats, null=True, blank=True, default=DEFAULT_STATS_ID, on_delete=models.CASCADE, related_name='base_stats')

    weapon = models.ForeignKey(Weapon, null=True,blank=True,  on_delete=models.CASCADE, related_name='weapon')
    helmet = models.ForeignKey(Item, null=True,blank=True,  on_delete=models.CASCADE, related_name='helmet')
    armor = models.ForeignKey(Item, null=True,blank=True,  on_delete=models.CASCADE, related_name='armor')
    graves = models.ForeignKey(Item, null=True,blank=True,  on_delete=models.CASCADE, related_name='graves')
    boots = models.ForeignKey(Item, null=True,blank=True,  on_delete=models.CASCADE, related_name='boots')
    necklase = models.ForeignKey(Item, null=True,blank=True,  on_delete=models.CASCADE, related_name='necklase')


    @property
    def exp_to_next_level(self):
        return self.level^3 - self.current_exp

    @property
    def total_stats(self):
        stats = self.base_stats + self.helmet + self.armor + self.graves + self.boots + self.necklase
        if self.weapon:
            stats += self.weapon.stats
        return stats
    
    def level_up(self):
        self.level += 1
        self.current_exp = 1

    def __str__(self):
        return self.nickname

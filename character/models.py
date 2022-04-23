from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Stats(models.Model):
    strength = models.IntegerField()
    agility = models.IntegerField()
    vitality = models.IntegerField()
    luck = models.IntegerField()

    def __add__(self, stats):
        strength = self.strength + stats.strength
        agility = self.agility + stats.agility
        vitality = self.vitality + stats.vitality
        luck = self.luck + stats.luck
        return Stats(strength, agility, vitality, luck)


class Character(models.Model):
    nickname = models.CharField(max_length=10)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)    
    level = models.IntegerField(default=1)
    current_exp = models.IntegerField(default=1)
    base_stats = models.ForeignKey(Stats, on_delete=models.CASCADE, related_name='base_stats')
    weapon_damage = models.IntegerField(default=1)
    weapon_stats = models.ForeignKey(Stats, on_delete=models.CASCADE, related_name='weapon_stats')
    helmet_stats = models.ForeignKey(Stats, on_delete=models.CASCADE, related_name='helmet_stats')
    armor_stats = models.ForeignKey(Stats, on_delete=models.CASCADE, related_name='armor_stats')
    graves_stats = models.ForeignKey(Stats, on_delete=models.CASCADE, related_name='graves_stats')
    boots_stats = models.ForeignKey(Stats, on_delete=models.CASCADE, related_name='boots_stats')
    necklase_stats = models.ForeignKey(Stats, on_delete=models.CASCADE, related_name='necklase_stats')


    @property
    def exp_to_next_level(self):
        return self.level^3

    def level_up(self):
        self.level += 1
        self.current_exp = 1

from common.models import Stats
from django.db import models

# Create your models here.


class Item(Stats):
    class ItemType(models.IntegerChoices):
        WEAPON = 1, "weapon"
        HELMET = 2, "helmet"
        ARMOR = 3, "armor"
        NECKLEASE = 4, "necklease"
        LEGGINGS = 5, "leggings"
        SHIELD = 6, "shield"

    name = models.CharField(null=True, max_length=30)
    type = models.PositiveSmallIntegerField(choices=ItemType.choices)
    damage = models.IntegerField(blank=True, default=0)
    block_chance = models.IntegerField(blank=True, null=True)
    equipped = models.BooleanField(null=True, blank=True, default=False)
    purchased = models.BooleanField(null=True, blank=True, default=False)
    price = models.IntegerField(null=True)
    belongs_to = models.ForeignKey("character.Character", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

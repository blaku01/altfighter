from django.db import models
from common.models import Stats
# Create your models here.

WEAPON = 1
HELMET = 2
ARMOR = 3
NECKLEASE = 4
LEGGINGS = 5
ITEM_TYPES = (
    (WEAPON, 'weapon'),
    (HELMET, 'helmet'),
    (ARMOR, 'armor'),
    (NECKLEASE, 'necklease'),
    (LEGGINGS, 'leggings'),
)

class Item(Stats):
    name = models.CharField(null=True, max_length=10)
    type = models.PositiveSmallIntegerField(
        choices=ITEM_TYPES
    )
    damage = models.IntegerField(blank=True, default=0)
    equipped = models.BooleanField(null=True, blank=True, default=False)
    purchased = models.BooleanField(null=True, blank=True, default=False)
    price = models.IntegerField(null=True)
    belongs_to = models.ForeignKey('character.Character', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from .models import Item
from character.factories import CharacterFactory

class ItemFactory(DjangoModelFactory):
    class Meta:
        model = Item

    name = Faker("name")
    type = 1
    belongs_to = SubFactory(CharacterFactory)
    price = 10
    damage = 5
    block_chance = 0
    strength = 1
    agility = 2
    vitality = 3
    luck = 4
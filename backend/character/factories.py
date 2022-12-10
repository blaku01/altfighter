from .models import Character
from factory import SubFactory
from users.factories import UserFactory
from factory.django import DjangoModelFactory



class CharacterFactory(DjangoModelFactory):
    created_by = SubFactory(UserFactory)
    nickname = "MyCharacter"
    type = Character.WARRIOR
    currency = 100
    level = 5

    class Meta:
        model = Character
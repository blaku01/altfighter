import factory
from ..models import Character

class CharacterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Character

    @factory.sequence
    def nickname(n):
        return f"character {n}"

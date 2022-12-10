import factory
from factory.django import DjangoModelFactory
from .models import User

class UserFactory(DjangoModelFactory):
    email = factory.Faker("email")
    spouse_name = factory.Faker("name")
    date_of_birth = factory.Faker("date_of_birth")

    class Meta:
        model = User

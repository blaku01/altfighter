from users.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from character.models import Character
from users.factories import UserFactory
from character.factories import CharacterFactory

class FightTestCase(APITestCase):
    def setUp(self):
        # Create a test user using the UserFactory
        self.user1 = UserFactory()
        token = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        # Create another test user using the UserFactory
        self.user2 = UserFactory()

        # Create a test character for the first user using the CharacterFactory
        self.character1 = CharacterFactory(created_by=self.user1, nickname="character1")

        # Create a test character for the second user using the CharacterFactory
        self.character2 = CharacterFactory(created_by=self.user2, nickname="character2")

        self.fighting_url = reverse("arena-fight", args=(self.character2.pk,))

    def test_start_fight(self):
        response = self.client.post(self.fighting_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fight_cooldown(self):
        self.client.post(self.fighting_url)
        character = Character.objects.filter(pk=self.character1.pk).first()
        self.assertLess(character.fight_cooldown, 0)

    def test_get_battle_points(self):
        self.client.post(self.fighting_url)
        character = Character.objects.filter(pk=self.character1.pk).first()
        self.assertNotEqual(character.battle_points, 0)

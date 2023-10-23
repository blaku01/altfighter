from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from character.models import Character


class FightTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        token = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        self.user2 = User.objects.create_user(username="user2", password="password")

        self.character1 = Character.objects.create(
            nickname="character1",
            strength=200,
            agility=200,
            vitality=200,
            luck=200,
            created_by=self.user1,
        )

        self.character2 = Character.objects.create(
            nickname="character2", created_by=self.user2
        )

        self.fighting_url = reverse("arena-fight", args=(self.character2.pk,))

    def test_start_fight(self):
        response = self.client.post(self.fighting_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fight_cooldown(self):
        self.client.post(self.fighting_url)
        # self.character1 is not updating after fight()
        character = Character.objects.filter(pk=self.character1.pk).first()
        self.assertLess(character.fight_cooldown, 0)

    def test_get_battle_points(self):
        self.client.post(self.fighting_url)
        character = Character.objects.filter(pk=self.character1.pk).first()
        self.assertNotEqual(character.battle_points, 0)

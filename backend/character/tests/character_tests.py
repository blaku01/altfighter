import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from character.models import Character
from item.models import Item


class CharacterCreateTestCase(APITestCase):

    character_create_url = reverse("character-list")

    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        token = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

    def test_character_create(self):
        response = self.client.post(
            self.character_create_url, {"nickname": "character"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_character_create_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(
            self.character_create_url, {"nickname": "character"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CharacterTotalStatsTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        token = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        self.character = Character.objects.create(
            nickname="character", created_by=self.user1
        )
        self.characters_url = reverse(
            "character-detail", kwargs={"pk": self.character.pk}
        )

    def test_total_stats(self):
        Item.objects.create(
            name="sword",
            type=1,
            equipped=True,
            strength=1,
            agility=2,
            belongs_to=self.character,
        )
        Item.objects.create(
            name="necklase",
            type=2,
            equipped=True,
            strength=1,
            agility=1,
            luck=3,
            belongs_to=self.character,
        )
        self.character.strength = 1
        self.character.agility = 1
        self.character.vitality = 1
        self.character.luck = 1

        total_stats = self.character.total_stats

        self.assertEqual(
            total_stats, {"strength": 3, "agility": 4, "vitality": 1, "luck": 4}
        )

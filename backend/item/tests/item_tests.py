import json

from character.models import Character, Item
from character.serializers import CharacterListSerializer, CharacterSerializer
from character.views import CharacterViewSet
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.routers import SimpleRouter
from rest_framework.test import APITestCase


class EquipTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        token = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        self.character = Character.objects.create(
            nickname="character", created_by=self.user1
        )

        self.item1 = Item.objects.create(
            name="sword", type=1, strength=1, agility=2, belongs_to=self.character
        )

        self.equip_url = reverse("backpack-equip", args=(self.item1.pk,))

    def test_equip_item(self):
        self.item1.equipped = False
        self.item1.purchased = True
        self.item1.save()
        response = self.client.get(self.equip_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item = Item.objects.get(pk=self.item1.pk)
        self.assertEqual(item.equipped, True)

    def test_equip_equipped_item(self):
        self.item1.purchased = True
        self.item1.equipped = True
        self.item1.save()

        response = self.client.get(self.equip_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_equip_not_purchased_item(self):
        self.item1.purchased = False
        self.item1.equipped = False
        self.item1.save()

        response = self.client.get(self.equip_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        item = Item.objects.get(pk=self.item1.pk)
        self.assertEqual(item.equipped, False)


class PurchaseTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        token = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        self.character = Character.objects.create(
            nickname="character", created_by=self.user1
        )

        self.item1 = Item.objects.create(
            name="sword",
            type=1,
            strength=1,
            agility=2,
            belongs_to=self.character,
            price=10,
        )

        self.equip_url = reverse("shop-purchase", args=(self.item1.pk,))

    def test_purchase_item(self):
        self.item1.purchased = False
        self.item1.equipped = False
        self.item1.save()
        self.character.currency = 20
        self.character.save()

        response = self.client.get(self.equip_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item = Item.objects.get(pk=self.item1.pk)
        self.assertEqual(item.purchased, True)

    def test_purchase_item_without_currency(self):
        self.item1.purchased = False
        self.item1.equipped = False
        self.item1.save()
        self.character.currency = 0
        self.character.save()

        response = self.client.get(self.equip_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        item = Item.objects.get(pk=self.item1.pk)
        self.assertEqual(item.purchased, False)

    def test_purchase_purchased_item(self):
        self.item1.purchased = True
        self.item1.equipped = False
        self.item1.save()
        self.character.currency = 20
        self.character.save()

        response = self.client.get(self.equip_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

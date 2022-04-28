from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.routers import SimpleRouter
from character.models import Character, Mission
from character.views import CharacterViewSet
from rest_framework import status

router = SimpleRouter()
router.register(r'characters', CharacterViewSet)
class MissionTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1',
                                            password='password')
        token = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.user2 = User.objects.create_user(username='user2',
                                            password='password')

        self.character1 = Character.objects.create(nickname='character1', strength=200, agility=200, vitality=200, luck=200, created_by=self.user1)

        self.character2 = Character.objects.create(nickname='character2', created_by=self.user2)

        self.view = CharacterViewSet()
        self.view.basename = router.get_default_basename(CharacterViewSet)
        self.view.request = None
        self.fighting_url = self.view.reverse_action("fight", (self.character1.pk, self.character2.pk))

    def test_start_fight(self):
        response = self.client.get(self.fighting_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fight_cooldown(self):
        self.client.get(self.fighting_url)
        self.assertLess(self.character1.fight_cooldown, 0)

    def test_get_battle_points(self):
        self.client.get(self.fighting_url)
        self.assertNotEqual(self.character1.battle_points, 1)

    def test_start_others_fight(self):
        others_fighting_url = self.view.reverse_action("fight", (self.character2.pk, self.character1.pk))
        response = self.client.get(others_fighting_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

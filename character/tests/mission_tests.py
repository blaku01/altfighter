import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.routers import SimpleRouter
from character.models import Character, Mission
from character.views import CharacterViewSet

router = SimpleRouter()
router.register(r'characters', CharacterViewSet)
class MissionTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1',
                                            password='password')
        token = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.character = Character.objects.create(nickname='character', created_by=self.user1)

        self.mission1 = Mission.objects.create(name='mission1', exp=10, currency=10, time='00:10:00', belongs_to=self.character)
        self.mission2 = Mission.objects.create(name='mission1', exp=15, currency=15, time='00:15:00', belongs_to=self.character)
        self.mission3 = Mission.objects.create(name='mission1', exp=20, currency=20, time='00:20:00', belongs_to=self.character)

        self.view = CharacterViewSet()
        self.view.basename = router.get_default_basename(CharacterViewSet)
        self.view.request = None
        self.mission_url = self.view.reverse_action("start_mission", (self.character.pk, self.mission1.id))
        self.missions_url = self.view.reverse_action("missions", (self.character.pk,))

    def test_start_mission(self):
        equip_url = self.view.reverse_action("start_mission", (self.character.pk, self.mission1.id))
        response = self.client.get(equip_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mission = Mission.objects.get(pk=self.mission1.pk)
        self.assertNotEqual(mission.time_started, None)

    def test_get_resources_from_mission(self):
        self.mission1.time = '00:00:00'
        self.mission1.save()

        self.client.get(self.mission_url)
        self.client.get(self.missions_url)

        character = Character.objects.filter(id=self.character.id)[0]
        self.assertEqual(character.current_exp, 5)
        self.assertEqual(character.level, 3)
        self.assertEqual(character.currency, 10)


    def test_start_second_mission(self):
        equip_url1 = self.view.reverse_action("start_mission", (self.character.pk, self.mission1.id))
        equip_url2 = self.view.reverse_action("start_mission", (self.character.pk, self.mission2.id))
        self.client.get(equip_url1)
        response = self.client.get(equip_url2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        mission = Mission.objects.get(pk=self.mission2.pk)
        self.assertEqual(mission.time_started, None)
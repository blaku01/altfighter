from datetime import datetime
import random

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.views import Response

from character.models import Character, Mission
from character.permissions import HasChampionAlready, IsObjectOwner
from character.serializers import (
    CharacterListSerializer,
    CharacterSerializer,
    MissionSerializer,
)
from character.tasks import refresh_character_missions, refresh_character_shops

import pytz
class MissionViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    # get mission list
    def list(self, request):
        print("starting")
        character = get_object_or_404(Character, created_by=request.user)
        # check if any of character missions has ended
        mission_ended = False
        print(f"\n\n\n\n {character.missions}")
        for mission in character.missions:
            print(f"\n mission {mission.time_started} \n")
            if mission.time_started is not None:
                if mission.has_finished:
                    mission_ended = mission
                    break
                # if mission has started - return only this mission
                if mission.has_started:
                    serialized_mission = MissionSerializer(
                        mission, many=False, context={"request": request}
                    ).data
                    return Response(serialized_mission, status=status.HTTP_200_OK)
        # if mission has finished grant character resources from it

        if mission_ended:
            print("MISSION ENDED! \n\n\n uwu")
            character.currency += mission_ended.currency
            character.current_exp += mission_ended.exp

            character.level_up_if_possible()

            character.save()

            refresh_character_missions(character)

        missions = character.missions
        serialized_missions = MissionSerializer(
            missions, many=True, context={"request": request}
        ).data
        return Response(serialized_missions, status=status.HTTP_200_OK)

    # take mission
    @action(
        detail=False,
        methods=["post"],
        url_path="start_mission/(?P<mission_pk>[^/.]+)",
        url_name="start_mission",
    )
    def start_mission(self, request, mission_pk):
        user_character = get_object_or_404(Character, created_by=request.user)
        user_missions = Mission.objects.filter(belongs_to=user_character)
        mission = user_missions.filter(pk=mission_pk).first()
        if mission:
            # check if user started another mission
            for user_mission in user_missions:
                if user_mission.has_started:
                    return Response(
                        {"status": "You already started a mission"},
                        status=status.HTTP_403_FORBIDDEN,
                    )
            # start and return mission
            mission.time_started = now()
            mission.save()
            serialized_mission = MissionSerializer(
                mission, context={"request": request}
            ).data
            return Response(serialized_mission, status=status.HTTP_200_OK)
        raise Http404

    # if mission has started - cancel it
    @action(
        detail=False,
        methods=["post", "delete"],
        url_path="cancel_mission/(?P<mission_pk>[^/.]+)",
        url_name="cancel_mission",
    )
    def cancel_mission(self, request, mission_pk):
        user_character = get_object_or_404(Character, created_by=request.user)
        user_mission = get_object_or_404(
            Mission, belongs_to=user_character, pk=mission_pk
        )
        if not user_mission.has_started:
            return Response(
                {"status": "You need to start mission first"},
                status=status.HTTP_403_FORBIDDEN,
            )
        user_mission.time_started = None
        user_mission.save()
        return Response(
            {"status": "Successfully canceled mission"}, status=status.HTTP_200_OK
        )


class ArenaViewSet(viewsets.ViewSet):
    def list(self, request):
        player_character = get_object_or_404(Character, created_by=request.user)
       # randomly generate 3 enemies with simillar battle_points
        characters = Character.objects.exclude(id=player_character.id).filter(
            battle_points__range=[
                player_character.battle_points - 100,
                player_character.battle_points + 100,
            ]
        ).order_by("?")[:3]
        serialized_characters = CharacterListSerializer(
            characters, many=True, context={"request": request}
        ).data
        return Response(serialized_characters, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["post", "get", "put"],
        url_path="fight/(?P<enemy_pk>[^/.]+)",
        url_name="fight",
    )
    def fight(self, request, enemy_pk):
        """
        This function simulates a fight between two characters.
        
        Inputs:
            request: HTTP request object
            enemy_pk: Primary key of the enemy character
        
        Output:
            HTTP status code and response data
        
        Assumptions/Limitations:
            - The function assumes that the enemy character exists and is accessible.
            - The function assumes that the player character has a valid `fight_cooldown` value.
        """
        
        # Get the player and enemy characters
        try:
            player_character = Character.objects.get(created_by=request.user)
            enemy_character = Character.objects.get(pk=enemy_pk)
        except Character.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
        # Return a 403 status code if the player character is on cooldown
        if player_character.fight_cooldown is None:
            return Response({}, status=status.HTTP_403_FORBIDDEN)
        
        # Set the last attacked time for the player character
        player_character.last_attacked_at = pytz.timezone('UTC').localize(datetime.utcnow())
        
        # Calculate the damage and critical hit chance for each character
        player_damage = player_character.damage
        player_hp_left = player_character.health
        player_crit_chance = player_character.calculate_crit(enemy_character)
        enemy_damage = enemy_character.damage
        enemy_hp_left = enemy_character.health
        enemy_crit_chance = enemy_character.calculate_crit(player_character)
        
        # Simulate the fight
        battle_log = []
        while True:
            player_damage_dealt = player_damage
            enemy_damage_dealt = enemy_damage
            
            # Calculate the enemy's damage
            if random.random() < enemy_crit_chance:
                enemy_damage_dealt *= 2
            
            # Enemy attacks first
            player_hp_left -= enemy_damage_dealt
            battle_log.append((enemy_damage_dealt, player_hp_left))
            
            # Check if the player has lost
            if player_hp_left < 0:
                player_character.battle_points -= 5
                player_character.save()
                print(battle_log)
                return Response({"battle_log": battle_log}, status=status.HTTP_200_OK)
            
            # Calculate the player's damage
            if random.random() < player_crit_chance:
                player_damage_dealt *= 2
            
            # Player attacks
            enemy_hp_left -= player_damage_dealt
            battle_log.append((player_damage_dealt, enemy_hp_left))
            
            # Check if the enemy has lost
            if enemy_hp_left < 0:
                player_character.battle_points += 10
                player_character.save()
                return Response({"battle_log": battle_log}, status=status.HTTP_200_OK)


class CharacterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Characters to be viewed.
    """

    permissions = [HasChampionAlready, IsObjectOwner]

    queryset = Character.objects.all().order_by("-battle_points")

    def get_serializer_class(self):
        if self.action == "list":
            return CharacterListSerializer
        else:
            return CharacterSerializer

    @action(detail=False, url_path="user_character", url_name="user_character")
    def get_user_character(self, request):
        refresh_character_shops.delay()
        user_character = get_object_or_404(Character, created_by=request.user)
        serialized_character = CharacterSerializer(
            user_character, context={"request": request}
        ).data
        return Response(serialized_character, status=status.HTTP_200_OK)

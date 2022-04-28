from multiprocessing.sharedctypes import Value

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework.views import Response

from character.models import Character, Item, Mission
from character.permissions import (DisallowPatch, DisallowPut,
                                   HasChampionAlready, IsOwnerObject)
from character.serializers import (CharacterListSerializer,
                                   CharacterSerializer, ItemSerializer,
                                   MissionSerializer, UserSerializer)
from character.tasks import refresh_character_missions, refresh_character_shops
from character.utils import when_mission_ends
import random


class CharacterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Characters to be viewed or edited.
    """
    queryset = Character.objects.all().order_by('-battle_points')


    permission_classes = [HasChampionAlready, IsOwnerObject, DisallowPatch, DisallowPut]

    def get_serializer_class(self):
        if self.action == 'list':
            return CharacterListSerializer
        else:
            return CharacterSerializer
    
    @action(detail=True, url_path='shop/(?P<item_pk>[^/.]+)', url_name='purchase_item')
    def purchase_item(self, request, item_pk, pk=None):
        item = get_object_or_404(Item, pk=item_pk)
        if item.belongs_to.created_by == request.user:
            if item.belongs_to.currency < item.price:
                return Response({'status': 'you dont have enough currency to purchase this item!'}, status=status.HTTP_403_FORBIDDEN)
            if len(item.belongs_to.backpack) > 5:
                return Response({'status': 'you dont have enough space in your backpack to purchase this item!'}, status=status.HTTP_403_FORBIDDEN)
            if item.purchased:
                return Response({'status': 'you already bought this item!'}, status=status.HTTP_403_FORBIDDEN)
            item.purchased = True
            item.belongs_to.currency -= item.price
            item.save()
            serialized_item = ItemSerializer(item, context={'request': request}).data
            return Response(serialized_item, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied({"message":"You don't have permission to access",
                                "object_id": item.id})

    @action(detail=True, url_path='shop', url_name='shop')
    def item_shop(self, request, pk=None):
        character = get_object_or_404(Character, pk=pk)
        if character.created_by == request.user:
            shop = character.shop
            serialized_item = ItemSerializer(shop, many=True, context={'request': request}).data
            return Response(serialized_item, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied({"message":"You don't have permission to access",
                                "object_id": character.id})

    @action(detail=True, url_path='backpack/(?P<item_pk>[^/.]+)', url_name='equip_item')
    def equip_item(self, request, item_pk, pk=None):
        item = get_object_or_404(Item, pk=item_pk)
        if item.belongs_to.created_by == request.user:

            if not item.purchased:
                return Response({'status': 'You need to purchase this item first'}, status=status.HTTP_403_FORBIDDEN)
            if item.equipped:
                return Response({'status': 'You have already equipped this item'}, status=status.HTTP_403_FORBIDDEN)
            # if item2 of the same type as item1 is equipped - unequip the item2 and equip item1
            if item.type in [item.type for item in item.belongs_to.equipped_items]:
                char = Character.objects.filter(created_by=request.user).first()
                item_eq = Item.objects.filter(belongs_to=char, equipped=True, name=item.name).first()
                item_eq.equipped = False
                item_eq.save()
                item.equipped = True
                item.save()
                serialized_item = ItemSerializer(item, context={'request': request}).data
                return Response(serialized_item, status=status.HTTP_200_OK)
            #equip item
            item.equipped = True
            item.save()
            serialized_item = ItemSerializer(item, context={'request': request}).data
            return Response(serialized_item, status=status.HTTP_200_OK)


        raise PermissionDenied({"message":"You don't have permission to access",
                            "object_id": item.id})

    @action(detail=True, url_path='backpack', url_name='backpack')
    def backpack(self, request, pk=None):
        character = get_object_or_404(Character, pk=pk)
        # check if its users backpack
        if character.created_by == request.user:
            backpack = character.backpack
            serialized_item = ItemSerializer(backpack, many=True, context={'request': request}).data
            return Response(serialized_item, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied({"message":"You don't have permission to access",
                                "object_id": character.id})
    
    @action(detail=True, url_path='missions/(?P<mission_pk>[^/.]+)', url_name='start_mission')
    def take_mission(self, request, mission_pk, pk):
        mission = get_object_or_404(Mission, pk=mission_pk)

        #check if its users character
        if mission.belongs_to.created_by == request.user:
            user_missions = Mission.objects.filter(belongs_to=mission.belongs_to)
            # if mission has started - cancel it and return every mission
            if mission.has_started:
                mission.time_started = None
                mission.save()
                return Response(MissionSerializer(user_missions, many=True, context={'request': request}).data, status=status.HTTP_200_OK)
            # check if user started another mission
            for user_mission in user_missions:
                if user_mission.has_started:
                    return Response({'status': 'You already started a mission'}, status=status.HTTP_403_FORBIDDEN)
                
            #start and return mission
            mission.time_started = now()
            mission.save()
            serialized_mission = MissionSerializer(mission, context={'request': request}).data
            return Response(serialized_mission, status=status.HTTP_200_OK)


        raise PermissionDenied({"message":"You don't have permission to access",
                            "object_id": mission.id})                                                                                                                            

    @action(detail=True, url_path='missions', url_name='missions')
    def missions(self, request, pk):
        character = get_object_or_404(Character, pk=pk)
        refresh_character_shops.delay()
        #check if its users character
        if character.created_by == request.user:
            #check if any of character missions has ended
            mission_ended = False
            for mission in character.missions:
                if mission.time_started is not None:
                    if mission.has_finished:
                        mission_ended = mission
                        break
                    # if mission has started - return only this mission
                    if mission.has_started:
                        serialized_mission = MissionSerializer(mission, many=False, context={'request':request}).data
                        return Response(serialized_mission, status=status.HTTP_200_OK)
            # if mission has finished grant character resources from it
            if mission_ended:
                character.currency += mission_ended.currency
                character.current_exp += mission_ended.exp

                character.level_up_if_possible()

                character.save()

                refresh_character_missions(character)

            missions = character.missions
            serialized_missions = MissionSerializer(missions, many=True, context={'request': request}).data
            return Response(serialized_missions, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied({"message":"You don't have permission to access",
                                "object_id": character.id})
    
    @action(detail=True, url_path='fight/(?P<enemy_pk>[^/.]+)', url_name='fight')
    def fight(self, request, enemy_pk, pk):
        player_character = get_object_or_404(Character, pk=pk)
        enemy_character = get_object_or_404(Character, pk=enemy_pk)

        #check if its users character
        if player_character.created_by == request.user:
            # if character fight is on cooldown, return 403
            if player_character.fight_cooldown is not None:
                player_dmg = player_character.damage
                player_hp_left = player_character.health
                player_crit_chance = player_character.calculate_crit(enemy_character)

                enemy_dmg = enemy_character.damage
                enemy_hp_left = enemy_character.health
                enemy_crit_chance = enemy_character.calculate_crit(player_character)
                battle_log = []
                while True:
                    player_damage_dealt = player_dmg
                    enemy_damage_dealt = enemy_dmg

                    if random.random() < enemy_crit_chance:
                        enemy_damage_dealt *= 2
                    # enemy always attacks firsts
                    player_hp_left -= enemy_dmg
                    battle_log.append((enemy_damage_dealt, player_hp_left))
                    if player_hp_left < 0:
                        return Response({'battle_log': battle_log}, status=status.HTTP_200_OK)

                    # player attacks
                    if random.random() < player_crit_chance:
                        player_damage_dealt *= 2
                    enemy_hp_left -= player_damage_dealt
                    if enemy_hp_left < 0:
                        return Response({'battle_log': battle_log}, status=status.HTTP_200_OK)
        

            return Response(status=status.HTTP_403_FORBIDDEN)


        raise PermissionDenied({"message":"You don't have permission to access",
                            "object_id": player_character.id})                                                                                                                            

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [DisallowPatch, DisallowPut]

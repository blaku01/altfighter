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
from character.tasks import refresh_character_missions
from character.utils import when_mission_ends

from numpy import power
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
            if item.name in [item.name for item in item.belongs_to.equipped_items]:
                char = Character.objects.filter(created_by=request.user).first()
                item_eq = Item.objects.filter(belongs_to=char, equipped=True, name=item.name).first()
                item_eq.equipped = False
                item_eq.save()
                item.equipped = True
                item.save()
                serialized_item = ItemSerializer(item, context={'request': request}).data
                return Response(serialized_item, status=status.HTTP_200_OK)

            item.equipped = True
            item.save()
            serialized_item = ItemSerializer(item, context={'request': request}).data
            return Response(serialized_item, status=status.HTTP_200_OK)


        raise PermissionDenied({"message":"You don't have permission to access",
                            "object_id": item.id})

    @action(detail=True, url_path='backpack', url_name='backpack')
    def backpack(self, request, pk=None):
        character = get_object_or_404(Character, pk=pk)
        if character.created_by == request.user:
            backpack = character.backpack
            serialized_item = ItemSerializer(backpack, many=True, context={'request': request}).data
            return Response(serialized_item, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied({"message":"You don't have permission to access",
                                "object_id": character.id})
    
    @action(detail=True, url_path='missions/(?P<item_pk>[^/.]+)', url_name='start_mission')
    def take_mission(self, request, item_pk, pk=None):
        mission = get_object_or_404(Mission, pk=item_pk)
        if mission.belongs_to.created_by == request.user:
            user_missions = Mission.objects.filter(belongs_to=mission.belongs_to)
            if mission.has_started:
                mission.time_started = None
                mission.save()
                return Response(MissionSerializer(user_missions, many=True, context={'request': request}).data, status=status.HTTP_200_OK)
            for user_mission in user_missions:
                if user_mission.has_started:
                    return Response({'status': 'You already started a mission'}, status=status.HTTP_403_FORBIDDEN)
                
            
            mission.time_started = now()
            mission.save()
            serialized_mission = MissionSerializer(mission, context={'request': request}).data
            return Response(serialized_mission, status=status.HTTP_200_OK)


        raise PermissionDenied({"message":"You don't have permission to access",
                            "object_id": mission.id})

    @action(detail=True, url_path='missions', url_name='missions')
    def missions(self, request, pk=None):
        character = get_object_or_404(Character, pk=pk)

        
        if character.created_by == request.user:
            mission_ended = False
            for mission in character.missions:
                if mission.time_started is not None:
                    to_mission_end = when_mission_ends(mission)
                    if to_mission_end < 0:
                        mission_ended = mission
                        break
            if mission_ended:
                character.currency += mission_ended.currency
                character.current_exp += mission_ended.exp
                
                while character.exp_to_next_level <= 0:
                    character.level += 1
                    character.current_exp = character.exp_to_next_level * -1

                character.save()
                mission_ended.delete()

                refresh_character_missions(character)

                missions = character.missions
                serialized_missions = MissionSerializer(missions, many=True, context={'request': request}).data
                return Response(serialized_missions, status=status.HTTP_200_OK)
            missions = character.missions
            serialized_missions = MissionSerializer(missions, many=True, context={'request': request}).data
            return Response(serialized_missions, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied({"message":"You don't have permission to access",
                                "object_id": character.id})
    
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

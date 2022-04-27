from multiprocessing.sharedctypes import Value
from rest_framework import viewsets, permissions
from character.serializers import CharacterSerializer, UserSerializer, ItemSerializer, CharacterListSerializer, MissionSerializer
from character.models import Character, Item, Mission
from django.contrib.auth.models import User
from character.permissions import HasChampionAlready, IsOwnerObject, DisallowPatch, DisallowPut
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import Response
from rest_framework.exceptions import APIException
from rest_framework.decorators import action
from character.tasks import refresh_character_missions
from django.utils.timezone import now
from character.utils import has_mission_ended, has_character_mission_ended

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
    
    @action(detail=True, url_path='purchase_item/(?P<item_pk>[^/.]+)')
    def purchase_item(self, request, item_pk, pk=None):
        item = get_object_or_404(Item, pk=item_pk)
        if item.belongs_to.created_by == request.user:
            if item.belongs_to.currency < item.price:
                raise APIException('you dont have enough currency to purchase this item!')
            if len(item.belongs_to.backpack) > 5:
                raise APIException('you dont have enough space in your backpack to purchase this item!')
            if item.purchased:
                raise APIException('you already bought this item!')
            item.purchased = True
            item.belongs_to.currency -= item.price
            item.save()
            serialized_item = ItemSerializer(item, context={'request': request}).data
            return Response(serialized_item)
        else:
            raise PermissionDenied({"message":"You don't have permission to access",
                                "object_id": item.id})

    @action(detail=True, url_path='purchase_item')
    def item_shop(self, request, pk=None):
        character = get_object_or_404(Character, pk=pk)
        if character.created_by == request.user:
            shop = character.shop
            serialized_item = ItemSerializer(shop, many=True, context={'request': request}).data
            return Response(serialized_item)
        else:
            raise PermissionDenied({"message":"You don't have permission to access",
                                "object_id": character.id})

    @action(detail=True, url_path='equip_item/(?P<item_pk>[^/.]+)')
    def equip_item(self, request, item_pk, pk=None):
        item = get_object_or_404(Item, pk=item_pk)
        if item.belongs_to.created_by == request.user:

            if not item.purchased:
                raise APIException('You need to purchase this item first')
            if item.equipped:
                raise APIException('You have already equipped this item')
            if item.name in [item.name for item in item.belongs_to.equipped_items]:
                char = Character.objects.filter(created_by=request.user).first()
                item_eq = Item.objects.filter(belongs_to=char, equipped=True, name=item.name).first()
                item_eq.equipped = False
                item_eq.save()
                item.equipped = True
                item.save()
                serialized_item = ItemSerializer(item, context={'request': request}).data
                return Response(serialized_item)

            item.equipped = True
            item.save()
            serialized_item = ItemSerializer(item, context={'request': request}).data
            return Response(serialized_item)


        raise PermissionDenied({"message":"You don't have permission to access",
                            "object_id": item.id})

    @action(detail=True, url_path='equip_item')
    def backpack(self, request, pk=None):
        character = get_object_or_404(Character, pk=pk)
        if character.created_by == request.user:
            backpack = character.backpack
            serialized_item = ItemSerializer(backpack, many=True, context={'request': request}).data
            return Response(serialized_item)
        else:
            raise PermissionDenied({"message":"You don't have permission to access",
                                "object_id": character.id})
    
    @action(detail=True, url_path='take_mission/(?P<item_pk>[^/.]+)')
    def take_mission(self, request, item_pk, pk=None):
        mission = get_object_or_404(Mission, pk=item_pk)
        has_mission_ended(mission)
        if mission.belongs_to.created_by == request.user:
            user_missions = Mission.objects.filter(belongs_to=mission.belongs_to)
            if mission.has_started:
                mission.time_started = None
                mission.save()
                return Response(MissionSerializer(user_missions, many=True, context={'request': request}).data)
            for user_mission in user_missions:
                if user_mission.has_started:
                    raise APIException('You already started a mission')
                
            
            mission.time_started = now()
            mission.save()
            serialized_mission = MissionSerializer(mission, context={'request': request}).data
            return Response(serialized_mission)


        raise PermissionDenied({"message":"You don't have permission to access",
                            "object_id": mission.id})

    @action(detail=True, url_path='take_mission')
    def missions(self, request, pk=None):
        character = get_object_or_404(Character, pk=pk)
        mission_ended = has_character_mission_ended(character)
        if mission_ended:
            character.currency += mission_ended.currency
            character.current_exp += mission_ended.exp
            
            while character.exp_to_next_level <= 0:
                character.level += 1
                character.exp = character.exp_to_next_level

            character.save()
            mission_ended.delete()

            refresh_character_missions()

            missions = character.missions
            serialized_item = MissionSerializer(missions, many=True, context={'request': request}).data
            return Response(serialized_item)

        
        if character.created_by == request.user:
            missions = character.missions
            serialized_item = MissionSerializer(missions, many=True, context={'request': request}).data
            return Response(serialized_item)
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

class StartMission(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        item = get_object_or_404(Item, pk=pk)
        if item.belongs_to.created_by == request.user:

            if not item.purchased:
                raise APIException('You need to purchase this item first')
            if item.equipped:
                raise APIException('You have already equipped this item')
            if item.name in [item.name for item in item.belongs_to.equipped_items]:
                char = Character.objects.filter(created_by=request.user).first()
                item_eq = Item.objects.filter(belongs_to=char, equipped=True, name=item.name).first()
                item_eq.equipped = False
                item_eq.save()
                item.equipped = True
                item.save()
                serialized_item = ItemSerializer(item, context={'request': request}).data
                return Response(serialized_item)

            item.equipped = True
            item.save()
            serialized_item = ItemSerializer(item, context={'request': request}).data
            return Response(serialized_item)


        raise PermissionDenied({"message":"You don't have permission to access",
                            "object_id": item.id})
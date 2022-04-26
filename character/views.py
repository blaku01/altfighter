from multiprocessing.sharedctypes import Value
from rest_framework import viewsets, permissions
from character.serializers import CharacterSerializer, UserSerializer, StatsSerializer, ItemSerializer, CharacterListSerializer
from character.models import Character, Stats, Item
from django.contrib.auth.models import User
from character.permissions import HasChampionAlready, IsOwnerObject, DisallowPatch, DisallowPut
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import Response
from rest_framework.exceptions import APIException
from rest_framework.decorators import action

class StatsViewSet(viewsets.ModelViewSet):
    queryset = Stats.objects.all()
    serializer_class = StatsSerializer
    permission_classes = [permissions.IsAdminUser]

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
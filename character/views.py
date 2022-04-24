from rest_framework import viewsets, permissions
from character.serializers import CharacterSerializer, UserSerializer, StatsSerializer, ItemSerializer, WeaponSerializer
from character.models import Character, Stats, Item, Weapon
from django.contrib.auth.models import User
from character.permissions import HasChampionAlready, IsOwnerObject

class StatsViewSet(viewsets.ModelViewSet):
    queryset = Stats.objects.all()
    serializer_class = StatsSerializer
    permission_classes = [permissions.IsAdminUser]

class CharacterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Characters to be viewed or edited.
    """
    queryset = Character.objects.all().order_by('-battle_points')
    serializer_class = CharacterSerializer
    permission_classes = [HasChampionAlready, IsOwnerObject]

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

class WeaponViewSet(viewsets.ModelViewSet):
    queryset = Weapon.objects.all()
    serializer_class = WeaponSerializer
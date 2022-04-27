from django.contrib.auth.models import User
from rest_framework import serializers

from character.models import Character, Item, Mission
from character.utils import when_mission_ends

class StatsSerializer(serializers.Serializer):
    strength=serializers.IntegerField(min_value=0)
    agility=serializers.IntegerField(min_value=0)
    vitality=serializers.IntegerField(min_value=0)
    luck=serializers.IntegerField(min_value=0)
    
class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ['id','name', 'price', 'strength', 'agility', 'vitality', 'luck']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class MissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mission
        fields = ['id', 'name', 'exp', 'currency', 'time', 'time_started']


class CharacterSerializer(serializers.HyperlinkedModelSerializer):
    total_stats = StatsSerializer(read_only=True)
    shop = ItemSerializer(many=True, read_only=True)
    equipped_items = ItemSerializer(many=True, read_only=True)
    backpack = ItemSerializer(many=True, read_only=True)
    missions = MissionSerializer(many=True, read_only=True)
    class Meta:
        model = Character
        fields = ['url', 'nickname', 'level', 'current_exp', 'currency', 'strength', 'agility', 'vitality', 'luck', 'total_stats', 'equipped_items', 'backpack', 'shop', 'missions']
        read_only_fields = ('level', 'battle_points', 'current_exp')
        # extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}} #doesnt work after changing created_by to OneToOneField
        depth = 0
    
    def get_total_stats(self, obj):
        return obj.total_stats

    def get_equipped_items(self, obj):
        return obj.equipped_items
    
    def get_backpack(self, obj):
        return obj.backpack
    
    def get_shop(self, obj):
        return obj.shop
    
    def get_missions(self, obj):
        return obj.missions
    
    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        representation['base_stats'] = {}
        representation['base_stats']['strength'] = representation.pop('strength')
        representation['base_stats']['agility'] = representation.pop('agility')
        representation['base_stats']['vitality'] = representation.pop('vitality')
        representation['base_stats']['luck'] = representation.pop('luck')
        return representation

    def create(self, validated_data):
        character = Character.objects.create(**validated_data,created_by=self.context['request'].user,strength=0, agility=0,vitality=0,luck=0)
        return character
    

class CharacterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['url', 'nickname', 'battle_points']


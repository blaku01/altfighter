from rest_framework import serializers
from character.models import Character, Stats, Item, Mission
from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from character.tasks import refresh_character_shops
import datetime

class StatsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stats
        fields = '__all__'

class ItemSerializer(serializers.HyperlinkedModelSerializer):
    stats = StatsSerializer()
    class Meta:
        model = Item
        fields = ['url','name', 'stats', 'price']

    
    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        stats_representation = representation.pop('stats')
        stats_representation.pop('url')
        for key in stats_representation:
            representation[key] = stats_representation[key]
        return representation

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class MissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mission
        fields = ['name', 'exp', 'currency', 'time']

class CharacterSerializer(serializers.HyperlinkedModelSerializer):
    total_stats = StatsSerializer(read_only=True)
    shop = ItemSerializer(many=True, read_only=True)
    equipped_items = ItemSerializer(many=True, read_only=True)
    backpack = ItemSerializer(many=True, read_only=True)
    missions = MissionSerializer(many=True, read_only=True)
    class Meta:
        model = Character
        fields = ['url', 'nickname', 'base_stats', 'total_stats', 'equipped_items', 'backpack', 'shop', 'missions']
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
        stats_representation = representation.pop('total_stats')
        stats_representation.pop('url')
        for key in stats_representation:
            representation[key] = stats_representation[key]
        return representation

    def create(self, validated_data):
        stats = Stats(strength=0, agility=0,vitality=0,luck=0)
        stats.save()
        character = Character.objects.create(**validated_data, base_stats = stats ,created_by=self.context['request'].user)
        return character
    

class CharacterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['url', 'nickname', 'battle_points']
    

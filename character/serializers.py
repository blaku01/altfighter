from rest_framework import serializers
from character.models import Character, Stats, Item, Weapon
from django.contrib.auth.models import User

class StatsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stats
        fields = '__all__'

class ItemSerializer(serializers.HyperlinkedModelSerializer):
    stats = StatsSerializer()
    class Meta:
        model = Item
        fields = ['name', 'stats']

class WeaponSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Weapon
        fields = '__all__'

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class CharacterSerializer(serializers.HyperlinkedModelSerializer):
    total_stats = StatsSerializer(read_only=True)
    
    class Meta:
        model = Character
        exclude= ('created_by',)
        read_only_fields = ('level', 'battle_points', 'current_exp')
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
        depth = 2
    
    def get_total_stats(self, obj):
        return obj.total_stats

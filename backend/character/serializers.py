from character.models import Character, Mission
from character.utils import when_mission_ends
from django.contrib.auth.models import User
from item.serializers import ItemSerializer
from rest_framework import serializers


class StatsSerializer(serializers.Serializer):
    strength = serializers.IntegerField(min_value=0)
    agility = serializers.IntegerField(min_value=0)
    vitality = serializers.IntegerField(min_value=0)
    luck = serializers.IntegerField(min_value=0)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class MissionSerializer(serializers.HyperlinkedModelSerializer):
    total_time = serializers.SerializerMethodField()

    class Meta:
        model = Mission
        fields = ["id", "name", "exp", "currency", "time", "total_time"]

    def get_total_time(self, obj):
        if obj.time_started == None:
            return None
        return int(when_mission_ends(obj))


class CharacterSerializer(serializers.HyperlinkedModelSerializer):
    total_stats = StatsSerializer(read_only=True)
    equipped_items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Character
        fields = [
            "nickname",
            "url",
            "level",
            "current_exp",
            "currency",
            "strength",
            "agility",
            "vitality",
            "luck",
            "equipped_items",
            "total_stats",
        ]
        read_only_fields = (
            "url",
            "level",
            "current_exp",
            "currency",
            "strength",
            "agility",
            "vitality",
            "luck",
            "equipped_items",
            "total_stats",
        )
        depth = 0

    def get_total_stats(self, obj):
        return obj.total_stats

    def get_equipped_items(self, obj):
        return obj.equipped_items

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["base_stats"] = {
            stat: representation.pop(stat)
            for stat in ["strength", "agility", "vitality", "luck"]
        }
        return representation

    def create(self, validated_data):
        character = Character.objects.create(
            **validated_data,
            created_by=self.context["request"].user,
            strength=0,
            agility=0,
            vitality=0,
            luck=0
        )
        return character


class CharacterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ["url", "nickname", "battle_points"]

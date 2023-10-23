from item.models import Item
from rest_framework import serializers


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Item
        fields = [
            "id",
            "name",
            "type",
            "price",
            "strength",
            "agility",
            "vitality",
            "luck",
            "damage",
        ]

    def get_type(self, obj):
        return obj.ItemType.choices[obj.type][1]

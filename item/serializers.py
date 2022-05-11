from rest_framework import serializers
from item.models import Item


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'type', 'price',
                  'strength', 'agility', 'vitality', 'luck', 'damage']

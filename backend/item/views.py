from character.models import Character
from django.shortcuts import get_object_or_404
from item.models import Item
from item.serializers import ItemSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.views import Response


class ShopViewSet(viewsets.ViewSet):
    def list(self, request):
        character = get_object_or_404(Character, created_by=request.user)
        shop = character.shop
        serialized_item = ItemSerializer(
            shop, many=True, context={"request": request}
        ).data
        return Response(serialized_item, status=status.HTTP_200_OK)

    # buy an item
    @action(
        detail=False,
        methods=["post", "get", "put"],
        url_path="purchase/(?P<item_pk>[^/.]+)",
        url_name="purchase",
    )
    def purchase(self, request, item_pk):
        character = get_object_or_404(Character, created_by=request.user)
        item = get_object_or_404(Item, pk=item_pk, belongs_to=character)
        if item.belongs_to.currency < item.price:
            return Response(
                {"status": "you dont have enough currency to purchase this item!"},
                status=status.HTTP_403_FORBIDDEN,
            )
        if len(item.belongs_to.backpack) > 5:
            return Response(
                {
                    "status": "you dont have enough space in your backpack to purchase this item!"
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        if item.purchased:
            return Response(
                {"status": "you already bought this item!"},
                status=status.HTTP_403_FORBIDDEN,
            )
        item.purchased = True
        item.belongs_to.currency -= item.price
        item.save()
        serialized_item = ItemSerializer(item, context={"request": request}).data
        return Response(serialized_item, status=status.HTTP_200_OK)


class BackpackViewSet(viewsets.ViewSet):
    def list(self, request):
        character = get_object_or_404(Character, created_by=request.user)
        backpack = character.backpack
        serialized_item = ItemSerializer(
            backpack, many=True, context={"request": request}
        ).data
        return Response(serialized_item, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["post", "get", "put"],
        url_path="equip/(?P<item_pk>[^/.]+)",
        url_name="equip",
    )
    def equip(self, request, item_pk):
        character = get_object_or_404(Character, created_by=request.user)
        item = get_object_or_404(Item, pk=item_pk, belongs_to=character)
        if not item.purchased:
            return Response(
                {"status": "You need to purchase this item first"},
                status=status.HTTP_403_FORBIDDEN,
            )
        if item.equipped:
            return Response(
                {"status": "You have already equipped this item"},
                status=status.HTTP_403_FORBIDDEN,
            )
        # if item2 of the same type as item1 is equipped - unequip the item2 and equip item1
        if item.type in [item.type for item in item.belongs_to.equipped_items]:
            char = Character.objects.filter(created_by=request.user).first()
            item_eq = Item.objects.filter(
                belongs_to=char, equipped=True, name=item.name
            ).first()
            item_eq.equipped = False
            item_eq.save()
            item.equipped = True
            item.save()
            serialized_item = ItemSerializer(item, context={"request": request}).data
            return Response(serialized_item, status=status.HTTP_200_OK)
        # equip item
        item.equipped = True
        item.save()
        serialized_item = ItemSerializer(item, context={"request": request}).data
        return Response(serialized_item, status=status.HTTP_200_OK)

    # sell item!
    @action(
        detail=False,
        methods=["post", "get", "put", "delete"],
        url_path="sell/(?P<item_pk>[^/.]+)",
        url_name="sell",
    )
    def sell(self, request, item_pk):
        character = get_object_or_404(Character, created_by=request.user)
        item = get_object_or_404(Item, pk=item_pk, belongs_to=character)
        character.currency += item.price / 2
        character.save()
        item.delete()
        return Response(
            {"status": "Successfully sold item!"}, status=status.HTTP_403_FORBIDDEN
        )

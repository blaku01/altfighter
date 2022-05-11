from character.models import Character, Item, Mission
from django.contrib import admin


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    pass


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    pass

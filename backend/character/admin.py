from django.contrib import admin
from character.models import Character, Mission, Item
# Register your models here.

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    pass

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass

@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    pass
from django.contrib import admin
from character.models import Character, Mission, Item
# Register your models here.

@admin.register(Character)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Item)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Mission)
class AuthorAdmin(admin.ModelAdmin):
    pass
from django.contrib import admin
from character.models import Character, Stats, Item
# Register your models here.

@admin.register(Character)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Stats)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Item)
class AuthorAdmin(admin.ModelAdmin):
    pass

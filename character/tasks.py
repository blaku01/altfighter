from celery import shared_task
from character.models import Item, Character, Stats
from django.db import connection
from django.contrib.auth.models import User
import datetime
import pytz
from numpy.random import rand, choice, randint


ITEM_TYPES = ['weapon', 'helmet', 'armor', 'necklease', 'leggings']
@shared_task
def refresh_character_shops():
    with connection.cursor() as cursor:
        today = datetime.datetime.now(pytz.utc) + datetime.timedelta(days=1)
        last_week = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=7)
        users_logged_within_week = User.objects.filter(last_login__range=(last_week, today)).distinct()

        for user in users_logged_within_week:
            character = Character.objects.filter(created_by=user).first()
            if character is not None:
                items = character.shop
                items.delete()
                lvl = character.level
                numbers = rand(6, 4) * lvl * 2
                names = choice(ITEM_TYPES, 6)
                damages = [randint(0, 10)*lvl if i == 'weapon' else 0 for i in names]
                stat_list = Stats.objects.bulk_create([Stats(strength=numbers[i][0], agility=numbers[i][1], vitality=numbers[i][2], luck=numbers[i][3]) for i in range(6)])

                items = Item.objects.bulk_create([Item(name=names[i], stats=stat_list[i], belongs_to=character, price=stat_list[i].calculate_total_stats(), damage=damages[i]) for i in range(6)])

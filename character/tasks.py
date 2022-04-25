from celery import Celery
from celery.schedules import crontab
from character.models import Item, Character, Stats
from django.contrib.auth.models import User
import datetime
import pytz
from numpy.random import rand, choice, randint

app = Celery()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour='*/2', minute=0),
        refresh_character_shops.s(),
    )

ITEM_TYPES = ['weapon', 'helmet', 'armor', 'necklease', 'leggings']
@app.task
def refresh_character_shops():
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


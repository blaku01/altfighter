import datetime

import pytz
from celery import shared_task
from django.contrib.auth.models import User
from django.db import connection
from numpy import ones, clip
from numpy.random import choice, rand, randint

from character.models import Character, Mission
from item.models import ITEM_TYPES, Item
from character.utils import generate_place_name, generate_item_name


@shared_task
def refresh_character_shops():
    with connection.cursor() as cursor:
        today = datetime.datetime.now(pytz.utc) + datetime.timedelta(days=1)
        last_week = datetime.datetime.now(
            pytz.utc) - datetime.timedelta(days=7)
        users_logged_within_week = User.objects.filter(
            last_login__range=(last_week, today)).distinct()

        for user in users_logged_within_week:
            character = Character.objects.filter(created_by=user).first()
            if character is not None:
                items = character.shop
                items.delete()
                lvl = character.level
                numbers = rand(6, 4) * lvl * 2
                # if character.type == WARRIOR -> ITEM CAN BE A SHIELD
                item_type_len = len(ITEM_TYPES) - 1
                if character.type == 'warrior':
                    item_type_len += 1
                types = randint(1, item_type_len + 1, 6)
                damages = [randint(0, 10)*lvl if type == 1 else 0 for type in types]
                block_chances = [clip(rand()* 10 * lvl, 0, 25) if type == 6 else 0 for type in types]
                items = Item.objects.bulk_create([Item(name=generate_item_name(), type=types[i], belongs_to=character, price=numbers[i][0] + numbers[i][1] + numbers[i][2] + numbers[i][3],
                                                       damage=damages[i], block_chance=block_chances[i], strength=numbers[i][0], agility=numbers[i][1], vitality=numbers[i][2], luck=numbers[i][3]) for i in range(6)])


@shared_task
def refresh_every_character_missions():
    with connection.cursor() as cursor:
        today = datetime.datetime.now(pytz.utc) + datetime.timedelta(days=1)
        last_week = datetime.datetime.now(
            pytz.utc) - datetime.timedelta(days=7)
        users_logged_within_week = User.objects.filter(
            last_login__range=(last_week, today)).distinct()

        for user in users_logged_within_week:
            character = Character.objects.filter(created_by=user).first()
            if character is not None:
                refresh_character_missions(character)


def refresh_character_missions(character):
    missions = character.missions
    missions.delete()
    lvl = character.level
    mission_times = randint(5, 15, size=3)
    gold = randint(5, 10, size=3) * lvl
    exp = 3 * lvl
    gold_exp_ratio = rand(3)
    exp_gold_ratio = ones(3) - gold_exp_ratio
    gold = gold * gold_exp_ratio * mission_times
    exp = exp_gold_ratio * exp * mission_times
    missions = Mission.objects.bulk_create([Mission(name=generate_place_name(
    ), exp=exp[i], currency=gold[i], time=f"00:{int(mission_times[i])}", belongs_to=character) for i in range(3)])

import datetime

import pytz
from celery import shared_task
from character.models import Character, Mission
from character.utils import generate_item_name, generate_place_name
from users.models import User
from django.db import connection
from numpy import clip, ones
from numpy.random import choice, rand, randint

from character.models import Character, Mission
from character.utils import generate_item_name, generate_place_name
from item.models import Item


@shared_task
def refresh_character_shops():
    now = datetime.datetime.now(pytz.utc)
    last_week = now - datetime.timedelta(days=7)
    today = now + datetime.timedelta(days=1)

    users_logged_within_week = User.objects.filter(
        last_login__range=(last_week, today)
    ).distinct()

    items = []
    for user in users_logged_within_week:
        character = Character.objects.filter(created_by=user).first()
        if character is not None:
            # Delete the existing items in the character's shop
            character.shop.delete()
            lvl = character.level
            numbers = rand(6, 4) * lvl * 2
            # if character.type == WARRIOR -> ITEM CAN BE A SHIELD
            # Generate the types list using a list comprehension
            item_types = [randint(1, len(Item.ItemType)) for _ in range(6)]

            # Use a dictionary to map item types to the corresponding damage value
            item_type_damages = {
                Item.ItemType.WEAPON: lambda lvl: randint(0, 10) * lvl,
                # Other item types have 0 damage
                Item.ItemType.ARMOR: lambda lvl: 0,
                Item.ItemType.NECKLEASE: lambda lvl: 0,
                Item.ItemType.LEGGINGS: lambda lvl: 0,
                Item.ItemType.SHIELD: lambda lvl: 0,
            }
            # Use a list comprehension to calculate the damages for each item
            # based on its type and level
            damages = [item_type_damages[type](lvl) for type in item_types]
            # Use the clip() method to ensure that the block_chances values are within the range 0 to 25
            block_chances = clip(rand(6) * 10 * lvl, 0, 25)

            # Generate the items for the character and append them to the items list
            items += [
                Item(
                    name=generate_item_name(),
                    type=item_types[i],
                    belongs_to=character,
                    price=numbers[i][0]
                    + numbers[i][1]
                    + numbers[i][2]
                    + numbers[i][3],
                    damage=damages[i],
                    block_chance=block_chances[i],
                    strength=numbers[i][0],
                    agility=numbers[i][1],
                    vitality=numbers[i][2],
                    luck=numbers[i][3],
                )
                for i in range(6)
            ]

    # Save all of the items to the database using the bulk_create() method
    Item.objects.bulk_create(items)


@shared_task
def refresh_every_character_missions():
    with connection.cursor() as cursor:
        today = datetime.datetime.now(pytz.utc) + datetime.timedelta(days=1)
        last_week = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=7)
        users_logged_within_week = User.objects.filter(
            last_login__range=(last_week, today)
        ).distinct()

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
    missions = Mission.objects.bulk_create(
        [
            Mission(
                name=generate_place_name(),
                exp=exp[i],
                currency=gold[i],
                time=f"00:{int(mission_times[i])}",
                belongs_to=character,
            )
            for i in range(3)
        ]
    )

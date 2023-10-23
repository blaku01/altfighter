# Generated by Django 4.1.3 on 2022-11-08 12:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("character", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("strength", models.IntegerField(blank=True, default=0, null=True)),
                ("agility", models.IntegerField(blank=True, default=0, null=True)),
                ("vitality", models.IntegerField(blank=True, default=0, null=True)),
                ("luck", models.IntegerField(blank=True, default=0, null=True)),
                ("name", models.CharField(max_length=10, null=True)),
                (
                    "type",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "weapon"),
                            (2, "helmet"),
                            (3, "armor"),
                            (4, "necklease"),
                            (5, "leggings"),
                            (6, "shield"),
                        ]
                    ),
                ),
                ("damage", models.IntegerField(blank=True, default=0)),
                ("block_chance", models.IntegerField(blank=True, null=True)),
                ("equipped", models.BooleanField(blank=True, default=False, null=True)),
                (
                    "purchased",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
                ("price", models.IntegerField(null=True)),
                (
                    "belongs_to",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="character.character",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

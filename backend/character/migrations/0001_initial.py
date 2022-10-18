# Generated by Django 4.0.8 on 2022-10-15 00:06

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strength', models.IntegerField(blank=True, default=0, null=True)),
                ('agility', models.IntegerField(blank=True, default=0, null=True)),
                ('vitality', models.IntegerField(blank=True, default=0, null=True)),
                ('luck', models.IntegerField(blank=True, default=0, null=True)),
                ('nickname', models.CharField(max_length=10, null=True, unique=True)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'warrior'), (2, 'hunter'), (3, 'mage')], null=True)),
                ('currency', models.IntegerField(blank=True, default=0, null=True)),
                ('level', models.IntegerField(blank=True, default=1, null=True)),
                ('battle_points', models.IntegerField(blank=True, default=0, null=True)),
                ('current_exp', models.IntegerField(blank=True, default=0, null=True)),
                ('last_attacked_at', models.DateTimeField(blank=True, default=datetime.datetime(1000, 1, 1, 1, 1, 1, 1, tzinfo=utc), null=True)),
                ('created_by', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True)),
                ('exp', models.IntegerField()),
                ('currency', models.IntegerField()),
                ('time', models.TimeField()),
                ('time_started', models.DateTimeField(blank=True, null=True)),
                ('belongs_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='character.character')),
            ],
        ),
    ]
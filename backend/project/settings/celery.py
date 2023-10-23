import os

from celery.schedules import crontab

CELERY_TIMEZONE = "Europe/Warsaw"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

CELERY_IMPORTS = ("character.tasks",)

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BACKEND", "redis://redis:6379/0")


CELERY_BEAT_SCHEDULE = {
    "refresh_character_shops": {
        "task": "character.tasks.refresh_character_shops",
        "schedule": crontab(minute="*/1"),
    },
    "refresh_every_character_missions": {
        "task": "character.tasks.refresh_every_character_missions",
        "schedule": crontab(hour="*/1"),
    },
}

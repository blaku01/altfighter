"""
https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html
"""
import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

app = Celery("project")

app.config_from_object("django.conf:settings", namespace="CELERY")

# discover and load tasks.py from from all registered Django apps
app.autodiscover_tasks()

import os

import dj_database_url

DATABASES = {
    "default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
    if os.environ.get("DATABASE_URL", "")
    else {
        "ENGINE": "django.db.backends." + os.environ.get("ENGINE_NAME"),
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

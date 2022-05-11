import os

from .base import DEBUG

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Email settings
EMAIL_USE_TLS = True
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "myemail@gmail.com")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "your_password")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))

from .base import BASE_DIR

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "static/"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / MEDIA_URL
# Enable WhiteNoise's GZip compression of static assets.
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

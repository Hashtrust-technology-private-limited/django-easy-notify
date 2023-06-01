"""
To be used by pytests to override default database settings.
"""

from django_notifications.settings import *  # noqa

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa
    }
}
BROKER_BACKEND = "memory"

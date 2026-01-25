from .base import * # noqa: F403, F401
from .base import BASE_DIR  # Esto confirma al editor que BASE_DIR existe

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

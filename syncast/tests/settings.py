# syncast/tests/settings.py

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "test"
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "syncast",  # or your test app label like "syncast_test"
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'tests' / 'test_db.sqlite3',  # <- inside your tests directory
    }
}

USE_TZ = True

AUTH_USER_MODEL = "auth.User"  # or your custom user model if testing that

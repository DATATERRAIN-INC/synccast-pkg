# syncast/tests/conftest.py

import django
from django.conf import settings

def pytest_configure():
    settings.configure(
        SECRET_KEY='test',
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'syncast',
        ],
        AUTH_USER_MODEL='auth.User',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        USE_TZ=True,
    )
    django.setup()

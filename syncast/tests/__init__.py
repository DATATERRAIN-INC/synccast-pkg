# tests/conftest.py or tests/__init__.py

import django
from django.conf import settings

def pytest_configure():
    settings.configure(
        DEBUG=True,
        SECRET_KEY='test',
        INSTALLED_APPS=[
            'syncast',  # Your package
            'django.contrib.auth',
            'django.contrib.contenttypes',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        USE_TZ=True,
    )
    django.setup()

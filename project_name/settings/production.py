"""
Production Settings
"""
from .base import *

APPS = []

INSTALLED_APPS += APPS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}

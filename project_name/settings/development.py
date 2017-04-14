"""
Development Settings
"""
from .base import *

DEBUG = True

APPS = [
]

INSTALLED_APPS += APPS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

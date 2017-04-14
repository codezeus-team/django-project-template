"""
Base Settings
"""
import os
import sys

# DEFINE PATHS
PROJECT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(PROJECT_DIR)
REPO_DIR = os.path.dirname(BASE_DIR)

APPS_DIR = os.path.join(BASE_DIR, 'apps')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
MEDIA_DIR = os.path.join(BASE_DIR, 'media')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

sys.path.insert(0, APPS_DIR)

# CORE SETTINGS
DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = []
ROOT_URLCONF = '{{project_name}}.urls'
WSGI_APPLICATION = '{{project_name}}.wsgi.application'
AUTH_USER_MODEL = 'user_auth.Account'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# APP DECLARATIONS
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'suit',
    'crispy_forms',
    'registration',
    'imagekit',
    'django_toolset',
    'django_extensions',
    'compressor',
]

LOCAL_APPS = [
    'landings',
    'user_auth',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE
MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# INTERNATIONALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# STATIC AND MEDIA FILES
STATIC_URL = '/static/'
STATIC_ROOT = STATIC_DIR

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_ENABLED = True
COMPRESS_ROOT = STATIC_ROOT

MEDIA_URL = '/media/'
MEDIA_ROOT = MEDIA_DIR

# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Password Settings
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# APP SPECFIC SETTINGS
CRISPY_TEMPLATE_PACK = 'bootstrap3'
ACCOUNT_ACTIVATION_DAYS = 7

# -*- coding: utf-8 -*-

import os

import syjon.config as config

# ------------------------------------------------------
# --- MISC
# ------------------------------------------------------

IS_READ_ONLY = config.IS_READ_ONLY

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SITE_ID = 1

ROOT_URLCONF = 'syjon.urls'

DJANGO_SETTINGS_MODULE = 'syjon.settings'
WSGI_APPLICATION = 'syjon.wsgi.application'


# ------------------------------------------------------
# --- MESSAGES
# ------------------------------------------------------

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


# ------------------------------------------------------
# --- EMAIL
# ------------------------------------------------------

EMAIL_HOST = config.EMAIL_HOST
EMAIL_PORT = config.EMAIL_PORT
EMAIL_HOST_USER = config.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = config.EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL = config.DEFAULT_FROM_EMAIL
EMAIL_USE_TLS = config.EMAIL_USE_TLS


# ------------------------------------------------------
# --- DATABASES
# ------------------------------------------------------

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': config.DB_NAME,
#         'USER': config.DB_USER,
#         'PASSWORD': config.DB_PASS,
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#     },
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config.DB_NAME,
        'USER': config.DB_USER,
        'PASSWORD': config.DB_PASS,
        'HOST': '127.0.0.1',
        'PORT': config.DB_PORT,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    },
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------------------------------------------
# --- SECURITY
# ------------------------------------------------------

DEBUG = config.DEBUG

INTERNAL_IPS = ('127.0.0.1',)
ALLOWED_HOSTS = (
    'sowa.umcs.pl',
    'www.sowa.umcs.pl',
    '127.0.0.1',
    'localhost',
)

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

LOGIN_URL = '/trainman/login/'

SECRET_KEY = config.SECRET_KEY

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'apps.trainman.backends.AdministrationModelBackend',
]

SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ------------------------------------------------------
# --- LANGUAGES
# ------------------------------------------------------

USE_I18N = True
USE_L10N = True
USE_TZ = True

TIME_ZONE = 'Europe/Warsaw'

gettext = lambda s: s

LANGUAGE_CODE = 'pl'

LANGUAGES = [
    ('pl', gettext('polish')),
    ('en', gettext('english')),
    ('ua', gettext('ukrainian')),
    ('ru', gettext('russian')),
]


# ------------------------------------------------------
# --- STATIC AND MEDIA FILES
# ------------------------------------------------------

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# ------------------------------------------------------
# --- CACHE
# ------------------------------------------------------

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'cache',
    }
}

# ------------------------------------------------------
# --- SESSION
# ------------------------------------------------------

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# ------------------------------------------------------
# --- TEMPLATES
# ------------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]


# ------------------------------------------------------
# --- MIDDLEWARE CLASSES
# ------------------------------------------------------

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'apps.syjon.middleware.ForceDefaultLanguageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]


# ------------------------------------------------------
# --- INSTALLED APPS
# ------------------------------------------------------

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',

    'apps.syjon',
    'apps.trainman',
    'apps.merovingian',
    'apps.trinity',
    'apps.metacortex',
    'apps.niobe',

    'modeltranslation',
    'django_extensions',
)

# ------------------------------------------------------
# --- MODEL TRANSLATION
# ------------------------------------------------------

MODELTRANSLATION_TRANSLATION_FILES = (
    'apps.trinity.translation',
    'apps.metacortex.translation',
    'apps.merovingian.translation',
)

MODELTRANSLATION_DEBUG = config.DEBUG


# ------------------------------------------------------
# --- DJANGO DEBUG TOOLBAR
# ------------------------------------------------------

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.cache.CachePanel',
]

# ------------------------------------------------------
# --- DJANGO ADMIN
# ------------------------------------------------------

ADMIN_SITE_HEADER = 'Administracja sowa'

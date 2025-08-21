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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config.DB_NAME,
        'USER': config.DB_USER,
        'PASSWORD': config.DB_PASS,
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },
}

# ------------------------------------------------------
# --- SECURITY
# ------------------------------------------------------

DEBUG = config.DEBUG

INTERNAL_IPS = ('127.0.0.1',)
ALLOWED_HOSTS = (
    '127.0.0.1',
    '212.182.11.15',
    'localhost',
    'syjon-0.umcs.lublin.pl',
    'syjon-1.umcs.lublin.pl',
    'syjon.umcs.lublin.pl',
)

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher'
)

LOGIN_URL = '/trainman/login/'

SECRET_KEY = config.SECRET_KEY

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'apps.trainman.backends.AdministrationModelBackend',
]

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
#    ('en', gettext('english')),
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
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
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

MIDDLEWARE_CLASSES = (
    'apps.syjon.middleware.ForceDefaultLanguageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)


# ------------------------------------------------------
# --- INSTALED APPS
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
    'apps.lock',

    'modeltranslation',
    'django_extensions',
    'floppyforms',
    'dbbackup'
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
# --- DB BACKUP DROPBOX
# ------------------------------------------------------

DBBACKUP_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
DBBACKUP_STORAGE_OPTIONS = {
    'oauth2_access_token': 'HOoVleYCb00AAAAAAABX_41xPAC0OeQLcad-FpJxd4ezBD92HebrFY5tib8L3gRs',
}

DBBACKUP_DATE_FORMAT = '%Y-%m-%d-%H-%M-%S'
DBBACKUP_FILENAME_TEMPLATE = '{databasename}-{datetime}.{extension}'
DBBACKUP_CLEANUP_KEEP = 3


# ------------------------------------------------------
# --- DJANGO ADMIN
# ------------------------------------------------------

ADMIN_SITE_HEADER = "Administracja Syjon"

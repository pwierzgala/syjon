from __future__ import absolute_import

import os

import django
from celery import Celery
from django.core.cache import cache
from django.core.management import call_command

# Path to project setting for lazy loaders.
settings_module = 'syjon.settings'

# Set the default Django setting module.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

# Without this line calling a task raised an exception:
# AppRegistryNotReady("Apps aren't loaded yet.")
django.setup()

# Create Celery application.
app = Celery("syjon")

# Load Celery settings.
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Set autodiscovery of Celery tasks.
app.autodiscover_tasks()


@app.task
def create_db_backup():
    """
    Creates database backup on Dropbox storage with 'dbbackup' command from
    django-dbbackup application.
    :return: None
    """
    call_command('dbbackup', compress=True, clean=True)


@app.task
def clear_sessions():
    """
    Clears django_session table.
    :return: None
    """
    cache.delete_pattern("*django.contrib.sessions*")

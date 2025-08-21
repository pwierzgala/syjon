"""
Created on 21-02-2013

@author: drusinek
"""

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


def fake_authenticate(username):
    backend = AdministrationModelBackend()
    user = backend.authenticate(username)
    if user:
        user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
    return user

class AdministrationModelBackend(ModelBackend):
    """
    Backend created to give possibility to authenticate user without password.
    Used only to temporary login to user from admin panel. 
    """

    def authenticate(self, username=None):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None


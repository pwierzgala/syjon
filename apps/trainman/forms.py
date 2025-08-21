# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput, required=True, label=_(u"Username"))
    password = forms.CharField(widget=forms.PasswordInput, label=_(u"Password"))


class UsernameForm(forms.Form):
    username = forms.CharField(min_length=2, max_length=30, required=False, label=_(u"Username"))


class EmailForm(forms.Form):
    email = forms.EmailField(label=_(u"E-mail"), required=False)

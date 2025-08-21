# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render

TEMPLATE_ROOT = 'syjon/'


def home(request):

    installed_apps = []
    for app_name in settings.INSTALLED_APPS:
        app_details = app_name.split('.')
        if app_details[0] == 'apps':
            installed_apps.append(app_details[1])

    kwargs = {'installed_apps': installed_apps}
    return render(request, TEMPLATE_ROOT+'syjon.html', kwargs)


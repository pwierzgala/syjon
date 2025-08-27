# -*- coding: utf-8 -*-

from django.conf import settings
from django.urls import include, re_path
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    re_path(
        r'',
        include(('apps.syjon.urls', 'syjon'), namespace='syjon')),
    re_path(
        r'^trainman/',
        include(('apps.trainman.urls', 'trainman'), namespace='trainman')),
    re_path(
        r'^merovingian/',
        include(('apps.merovingian.urls', 'merovingian'), namespace='merovingian')),
    re_path(
        r'^trinity/',
        include(('apps.trinity.urls', 'trinity'), namespace='trinity')),
    re_path(
        r'^metacortex/',
        include(('apps.metacortex.urls', 'metacortex'), namespace='metacortex')),
    re_path(
        r'^niobe/',
        include(('apps.niobe.urls', 'niobe'), namespace='niobe')),

    re_path(r'^admin/', admin.site.urls),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
]

admin.site.site_header = settings.ADMIN_SITE_HEADER

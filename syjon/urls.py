# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'', include('apps.syjon.urls', namespace='syjon')),
    url(r'^trainman/', include('apps.trainman.urls', namespace='trainman')),
    url(r'^merovingian/', include('apps.merovingian.urls', namespace='merovingian')),
    url(r'^trinity/', include('apps.trinity.urls', namespace='trinity')),
    url(r'^metacortex/', include('apps.metacortex.urls', namespace='metacortex')),
    url(r'^niobe/', include('apps.niobe.urls', namespace='niobe')),

    url(r'^lock/', include('apps.lock.urls', namespace='lock')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]

admin.site.site_header = settings.ADMIN_SITE_HEADER

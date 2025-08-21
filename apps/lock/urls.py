# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'item/(?P<id_item>\d+)', views.show_item, name='details'),
    url(r'print_receipt/(?P<id_item>\d+)', views.print_receipt, name='print'),
    url(r'^$', views.index, name='list')
]

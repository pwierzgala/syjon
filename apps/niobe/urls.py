# -*- coding: utf-8 -*-

from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        r'^$',
        views.index,
        name='course-list'
    ),
    re_path(
        r'^course/(?P<course_id>\d+)/modules/?$',
        views.course_modules,
        name='module-list'
    ),
    re_path(
        r'^course/(?P<course_id>\d+)/module/(?P<module_id>\d+)/subjects/?$',
        views.course_subjects,
        name='subject-list'
    ),
    re_path(
        r'^course/(?P<course_id>\d+)/module/(?P<module_id>\d+)/subject/(?P<subject_id>\d+)/?$',
        views.subject_show,
        name='subject-details'
    ),
    re_path(
        r'^teacher/show/?$',
        views.teacher_list,
        name='teacher-list'
    ),
]

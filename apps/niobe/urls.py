# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.index,
        name='course-list'
    ),
    url(
        r'^course/(?P<course_id>\d+)/modules/?$',
        views.course_modules,
        name='module-list'
    ),
    url(
        r'^course/(?P<course_id>\d+)/module/(?P<module_id>\d+)/subjects/?$',
        views.course_subjects,
        name='subject-list'
    ),
    url(
        r'^course/(?P<course_id>\d+)/module/(?P<module_id>\d+)/subject/(?P<subject_id>\d+)/?$',
        views.subject_show,
        name='subject-details'
    ),
    url(
        r'^teacher/show/?$',
        views.teacher_list,
        name='teacher-list'
    ),
]

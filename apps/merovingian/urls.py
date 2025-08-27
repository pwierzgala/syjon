# -*- coding: utf-8 -*-

from django.urls import include, re_path

from .views import course, management, merovingian, module, sgroup

course_urlpatterns = [
    re_path(
        r'^list/$',
        course.index, name='list'
    ),
    re_path(
        r'^(?P<department_id>\d+)/list/$',
        course.index, name='list'
    ),
    re_path(
        r'^add/?$',
        course.add, name='add'
    ),
    re_path(
        r'^(?P<course_id>\d+)/edit/$',
        course.edit, name='edit'
    ),
    re_path(
        r'^(?P<course_id>\d+)/name/$',
        course.name, name='details-name'
    ),
    re_path(
        r'^(?P<course_id>\d+)/show/$',
        course.show, name='details'
    ),
]

sgroup_urlpatterns = [
    re_path(
        r'^(?P<sgroup_id>\d+)/plan/$',
        sgroup.studies_plan, name='plan'
    ),
]

module_urlpatterns = [
    re_path(
        r'^sgroup/(?P<sgroup_id>\d+)/list/$',
        module.list, name='list'
    ),
    re_path(
        r'^sgroup/(?P<sgroup_id>\d+)/add/$',
        module.add, name='add'
    ),
    re_path(
        r'^(?P<module_id>\d+)/edit/$',
        module.edit, name='edit'
    ),
    re_path(
        r'^(?P<module_id>\d+)/delete/$',
        module.delete, name='delete'
    ),
    re_path(
        r'^(?P<module_id>\d+)/syllabuses$',
        module.syllabuses, name='syllabuses'
    ),
]

urlpatterns = [
    re_path(
        r'course/',
        include((course_urlpatterns, 'course'), namespace='course')),
    re_path(
        r'sgroup/',
        include((sgroup_urlpatterns, 'sgroup'), namespace='sgroup')),
    re_path(
        r'module/',
        include((module_urlpatterns, 'module'), namespace='module')),
    re_path(
        r'management/list/',
        management.index, name='management-list'
    ),
    re_path(
        r'^delete/confirm/$',
        merovingian.delete_confirm, name='delete-confirm'
    ),
    re_path(
        r'management/',
        merovingian.management, name='management'
    ),
    re_path(
        r'',
        merovingian.index, name='index'
    ),
]

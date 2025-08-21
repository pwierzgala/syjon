# -*- coding: utf-8 -*-

from django.conf.urls import include, url

from .views import course, management, merovingian, module, sgroup

course_urlpatterns = [
    url(
        r'^list/$',
        course.index, name='list'
    ),
    url(
        r'^(?P<department_id>\d+)/list/$',
        course.index, name='list'
    ),
    url(
        r'^add/?$',
        course.add, name='add'
    ),
    url(
        r'^(?P<course_id>\d+)/edit/$',
        course.edit, name='edit'
    ),
    url(
        r'^(?P<course_id>\d+)/name/$',
        course.name, name='details-name'
    ),
    url(
        r'^(?P<course_id>\d+)/show/$',
        course.show, name='details'
    ),
]

sgroup_urlpatterns = [
    url(
        r'^(?P<sgroup_id>\d+)/plan/$',
        sgroup.studies_plan, name='plan'
    ),
]

module_urlpatterns = [
    url(
        r'^sgroup/(?P<sgroup_id>\d+)/list/$',
        module.list, name='list'
    ),
    url(
        r'^sgroup/(?P<sgroup_id>\d+)/add/$',
        module.add, name='add'
    ),
    url(
        r'^(?P<module_id>\d+)/edit/$',
        module.edit, name='edit'
    ),
    url(
        r'^(?P<module_id>\d+)/delete/$',
        module.delete, name='delete'
    ),
    url(
        r'^(?P<module_id>\d+)/syllabuses$',
        module.syllabuses, name='syllabuses'
    ),
]

urlpatterns = [
    url(r'course/', include(course_urlpatterns, namespace='course')),
    url(r'sgroup/', include(sgroup_urlpatterns, namespace='sgroup')),
    url(r'module/', include(module_urlpatterns, namespace='module')),
    url(
        r'management/list/',
        management.index, name='management-list'
    ),
    url(
        r'^delete/confirm/$',
        merovingian.delete_confirm, name='delete-confirm'
    ),
    url(
        r'management/',
        merovingian.management, name='management'
    ),
    url(
        r'',
        merovingian.index, name='index'
    ),
]

# -*- coding: utf-8 -*-

from django.conf.urls import include, url

from apps.trinity.views.reform_2019 import clo as clo_2019
from apps.trinity.views.reform_2019 import ld
from apps.trinity.views.reform_2019 import mlo as mlo_2019
from apps.trinity.views.reform_2019 import slo as slo_2019

from .views import clo, ea, mlo

education_area_url_patterns = [
    url(
        r'assign/course/(?P<course_id>\d+)$',
        ea.assign, name='assign'
    ),
    url(
        r'assign_phd/course/(?P<course_id>\d+)$',
        ea.assign_phd, name='assign_phd'
    ),
]


course_learning_outcomes_url_patterns = [
    url(
        r'select-category/course/(?P<course_id>\d+)$',
        clo.education_category_select, name='select_category'
    ),
    url(
        r'show/course/(?P<course_id>\d+)/category/(?P<education_category_id>\d+)$',
        clo.show, name='show'
    ),
    url(
        r'add/course/(?P<course_id>\d+)/category/(?P<education_category_id>\d+)$',
        clo.add, name='add'
    ),
    url(
        r'update/course/(?P<course_id>\d+)/category/(?P<education_category_id>\d+)/clo/(?P<clo_id>\d+)$',
        clo.update, name='update'
    ),
    url(
        r'delete/course/(?P<course_id>\d+)/category/(?P<education_category_id>\d+)$',
        clo.delete, name='delete'
    ),
    url(
        r'pdf/course/(?P<course_id>\d+)$',
        clo.print_pdf, name='pdf'
    ),
]

module_learning_outcomes_url_patterns = [
    url(
        r'select-sgroup/course/(?P<course_id>\d+)$',
        mlo.select_sgroup, name='select_sgroup'
    ),
    url(
        r'select-module/course/(?P<course_id>\d+)/sgroup/(?P<sgroup_id>\d+)$',
        mlo.select_module, name='select_module'
    ),
    url(
        r'show/course/(?P<course_id>\d+)/sgroup/(?P<sgroup_id>\d+)/module/(?P<module_id>\d+)$',
        mlo.show, name='show'
    ),
    url(
        r'add/course/(?P<course_id>\d+)/sgroup/(?P<sgroup_id>\d+)/module/(?P<module_id>\d+)$',
        mlo.add, name='add'
    ),
    url(
        r'update/course/(?P<course_id>\d+)/sgroup/(?P<sgroup_id>\d+)/module/(?P<module_id>\d+)/mlo/(?P<mlo_id>\d+)$',
        mlo.update, name='update'
    ),
    url(
        r'delete/course/(?P<course_id>\d+)/sgroup/(?P<sgroup_id>\d+)/module/(?P<module_id>\d+)$',
        mlo.delete, name='delete'
    ),
    url(
        r'pdf/course/(?P<course_id>\d+)/sgroup/(?P<sgroup_id>\d+)/module/(?P<module_id>\d+)$',
        mlo.print_pdf, name='pdf'
    ),
]

leading_discipline_url_patterns = [
    url(
        r'assign/leading_discipline/(?P<course_id>\d+)$',
        ld.assign, name='assign'
    ),
]

subject_learning_outcomes_url_patterns = [
    url(
        r'select-sgroup/course/(?P<course_id>\d+)$',
        slo_2019.select_sgroup, name='select_sgroup'
    ),
    url(
        r'select-module/course/(?P<course_id>\d+)/sgroup/(?P<sgroup_id>\d+)$',
        slo_2019.select_module, name='select_module'
    ),
    url(
        r'select-subject/course/(?P<course_id>\d+)/sgroup/(?P<sgroup_id>\d+)/module/(?P<module_id>\d+)$',
        slo_2019.select_subject, name='select_subject'
    ),
    url(
        r'show/course/(?P<course_id>\d+)/sgroup/(?P<sgroup_id>\d+)/module/(?P<module_id>\d+)/subject/(?P<subject_id>\d+)$',
        slo_2019.show, name='show'
    ),
    url(
        r'update/course/(?P<course_id>\d+)/sgroup/(?P<sgroup_id>\d+)/module/(?P<module_id>\d+)/subject/(?P<subject_id>\d+)$',
        slo_2019.update, name='update'
    )
]

urlpatterns = [
    url(
        r'ea/',
        include(education_area_url_patterns, namespace='ea')
    ),
    url(
        r'clo/',
        include(course_learning_outcomes_url_patterns, namespace='clo')
    ),
    url(
        r'mlo/',
        include(module_learning_outcomes_url_patterns, namespace='mlo')
    ),
    url(
        r'ld/',
        include(leading_discipline_url_patterns, namespace="ld")
    ),
    url(
        r'slo/',
        include(subject_learning_outcomes_url_patterns, namespace='slo')
    ),
]

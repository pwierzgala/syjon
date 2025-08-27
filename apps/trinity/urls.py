# -*- coding: utf-8 -*-

from django.urls import include, re_path

from apps.trinity.views.reform_2019 import clo as clo_2019
from apps.trinity.views.reform_2019 import ld
from apps.trinity.views.reform_2019 import mlo as mlo_2019
from apps.trinity.views.reform_2019 import slo as slo_2019

from .views import clo, ea, mlo

education_area_url_patterns = [
    re_path(
        r'assign/course/(?P<course_id>\d+)$',
        ea.assign, name='assign'
    ),
    re_path(
        r'assign_phd/course/(?P<course_id>\d+)$',
        ea.assign_phd, name='assign_phd'
    ),
]


course_learning_outcomes_url_patterns = [
    re_path(
        r'select-category/course/(?P<course_id>\d+)$',
        clo.education_category_select, name='select_category'
    ),
    re_path(
        r'show/course/(?P<course_id>\d+)/category/(?P<education_category_id>\d+)$',
        clo.show, name='show'
    ),
    re_path(
        r'add/course/(?P<course_id>\d+)/category/(?P<education_category_id>\d+)$',
        clo.add, name='add'
    ),
    re_path(
        r'update/course/(?P<course_id>\d+)/category/(?P<education_category_id>\d+)/clo/(?P<clo_id>\d+)$',
        clo.update, name='update'
    ),
    re_path(
        r'delete/course/(?P<course_id>\d+)/category/(?P<education_category_id>\d+)$',
        clo.delete, name='delete'
    ),
    re_path(
        r'pdf/course/(?P<course_id>\d+)$',
        clo.print_pdf, name='pdf'
    ),
]

module_learning_outcomes_url_patterns = [
    re_path(
        r'select-sgroup/course/(?P<course_id>\d+)$',
        mlo.select_sgroup, name='select_sgroup'
    ),
    re_path(
        r'select-module/course/(?P<course_id>\d+)/sgroup/(?P<sgroup_id>\d+)$',
        mlo.select_module, name='select_module'
    ),
    re_path(
        r'show/course/(?P<course_id>\d+)/sgroup/(?P<sgroup_id>\d+)/module/(?P<module_id>\d+)$',
        mlo.show, name='show'
    ),
    re_path(
        r'add/course/(?P<course_id>\d+)/sgroup/(?P<sgroup_id>\d+)/module/(?P<module_id>\d+)$',
        mlo.add, name='add'
    ),
    re_path(
        r'update/course/(?P<course_id>\d+)/sgroup/(?P<sgroup_id>\d+)/module/(?P<module_id>\d+)/mlo/(?P<mlo_id>\d+)$',
        mlo.update, name='update'
    ),
    re_path(
        r'delete/course/(?P<course_id>\d+)/sgroup/(?P<sgroup_id>\d+)/module/(?P<module_id>\d+)$',
        mlo.delete, name='delete'
    ),
    re_path(
        r'pdf/course/(?P<course_id>\d+)/sgroup/(?P<sgroup_id>\d+)/module/(?P<module_id>\d+)$',
        mlo.print_pdf, name='pdf'
    ),
]

leading_discipline_url_patterns = [
    re_path(
        r'assign/leading_discipline/(?P<course_id>\d+)$',
        ld.assign, name='assign'
    ),
]

subject_learning_outcomes_url_patterns = [
    re_path(
        r'select-sgroup/course/(?P<course_id>\d+)$',
        slo_2019.select_sgroup, name='select_sgroup'
    ),
    re_path(
        r'select-module/course/(?P<course_id>\d+)/sgroup/(?P<sgroup_id>\d+)$',
        slo_2019.select_module, name='select_module'
    ),
    re_path(
        r'select-subject/course/(?P<course_id>\d+)/sgroup/(?P<sgroup_id>\d+)/module/(?P<module_id>\d+)$',
        slo_2019.select_subject, name='select_subject'
    ),
    re_path(
        r'show/course/(?P<course_id>\d+)/sgroup/(?P<sgroup_id>\d+)/module/(?P<module_id>\d+)/subject/(?P<subject_id>\d+)$',
        slo_2019.show, name='show'
    ),
    re_path(
        r'update/course/(?P<course_id>\d+)/sgroup/(?P<sgroup_id>\d+)/module/(?P<module_id>\d+)/subject/(?P<subject_id>\d+)$',
        slo_2019.update, name='update'
    )
]

urlpatterns = [
    re_path(
        r'ea/',
        include((education_area_url_patterns, 'ea'), namespace='ea')
    ),
    re_path(
        r'clo/',
        include((course_learning_outcomes_url_patterns, 'clo'), namespace='clo')
    ),
    re_path(
        r'mlo/',
        include((module_learning_outcomes_url_patterns, 'mlo'), namespace='mlo')
    ),
    re_path(
        r'ld/',
        include((leading_discipline_url_patterns, 'ld'), namespace="ld")
    ),
    re_path(
        r'slo/',
        include((subject_learning_outcomes_url_patterns, 'slo'), namespace='slo')
    ),
]

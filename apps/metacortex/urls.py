# -*- coding: utf-8 -*-

from django.urls import include, re_path

from .views import browser, metacortex, search_engine, syllabus_my

my_urlpatterns = [
    re_path(
        r'show/$',
        syllabus_my.show,
        name='show'
    ),
    re_path(
        r'syllabus-delete-ects/(?P<syllabus_type>\d+)/(?P<syllabus_id>\d+)/(?P<ects_id>\d+)$',
        syllabus_my.syllabus_delete_ects,
        name='delete_ects'
    ),
    re_path(
        r'syllabus-module-show/(?P<syllabus_id>\d+)$',
        syllabus_my.syllabus_module_show,
        name='show_module'
    ),
    re_path(
        r'syllabus-module-edit/(?P<syllabus_id>\d+)$',
        syllabus_my.syllabus_module_edit,
        name='edit_module'
    ),
    re_path(
        r'syllabus-module-print/(?P<syllabus_id>\d+)$',
        syllabus_my.syllabus_module_print,
        name='print_module'
    ),
    re_path(
        r'syllabus-subject-show/(?P<syllabus_id>\d+)$',
        syllabus_my.syllabus_subject_show,
        name='show_subject'
    ),
    re_path(
        r'syllabus-subject-edit/(?P<syllabus_id>\d+)$',
        syllabus_my.syllabus_subject_edit,
        name='edit_subject'
    ),
    re_path(
        r'syllabus-subject-print/(?P<syllabus_id>\d+)$',
        syllabus_my.syllabus_subject_print,
        name='print_subject'
    ),

    re_path(
        r'syllabus-module-copy-list/(?P<syllabus_id>\d+)$',
        syllabus_my.syllabus_module_copy_list,
        name='module_copy_list'
    ),
    re_path(
        r'syllabus-module-copy/(?P<syllabus_to_id>\d+)/(?P<syllabus_from_id>\d+)$',
        syllabus_my.syllabus_module_copy,
        name='copy_module'
    ),
    re_path(
        r'syllabus-subject-copy-list/(?P<syllabus_id>\d+)$',
        syllabus_my.syllabus_subject_copy_list,
        name='subject_copy_list'
    ),
    re_path(
        r'syllabus-subject-copy/(?P<syllabus_to_id>\d+)/(?P<syllabus_from_id>\d+)$',
        syllabus_my.syllabus_subject_copy,
        name='copy_subject'
    ),
    
    re_path(
        r'syllabus-practice-show/(?P<syllabus_id>\d+)$',
        syllabus_my.syllabus_practice_show,
        name='show_practice'
    ),
    re_path(
        r'syllabus-practice-edit/(?P<syllabus_id>\d+)$',
        syllabus_my.syllabus_practice_edit,
        name='edit_practice'
    ),
    re_path(
        r'syllabus-practice-print/(?P<syllabus_id>\d+)$',
        syllabus_my.syllabus_practice_print,
        name='print_practice'
    ),
]

search_urlpatterns = [
    re_path(
        r'search-classic/$',
        search_engine.syllabus_search_classic,
        name='classic'
    ),
    re_path(
        r'show/(?P<syllabus_type>\d{1})/(?P<syllabus_id>\d+)$',
        search_engine.syllabus_show,
        name='show'
    ),
]

browser_urlpatterns = [
    re_path(
        r'syllabus/select/(?P<course_id>\d+)$',
        browser.select_semester,
        name='select_semester'
    ),
    re_path(
        r'syllabus/browse/(?P<course_id>\d+)/(?P<semester>\d+)$',
        browser.browse,
        name='browse'
    ),
    re_path(
        r'syllabus/supervise/(?P<course_id>\d+)/(?P<semester>\d+)$',
        browser.supervise,
        name='supervise'
    ),
]


urlpatterns = [
    re_path(r'my/', include((my_urlpatterns, 'my'), namespace='my')),
    re_path(r'search/', include((search_urlpatterns, 'search'), namespace='search')),
    re_path(r'browse/', include((browser_urlpatterns, 'browse'), namespace='browser')),
    re_path(
        r'^confirm/(?P<syllabus_to_id>\d+)/(?P<syllabus_from_id>\d+)?$',
        metacortex.confirm,
        name='confirm'
    ),
    re_path(
        r'confirm/sm/(?P<syllabus_to_id>\d+)/(?P<syllabus_from_id>\d+)?$',
        metacortex.confirm_sm,
        name='confirm_sm'
    ),
    re_path(
        r'help$',
        metacortex.show_help,
        name='help'
    ),
]

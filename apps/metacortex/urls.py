# -*- coding: utf-8 -*-

from django.conf.urls import include, url

from .views import browser, metacortex, search_engine, syllabus_my

my_urlpatterns = [
    url(
        r'show/$',
        syllabus_my.show,
        name='show'
    ),
    url(
        r'syllabus-delete-ects/(?P<syllabus_type>\d+)/(?P<syllabus_id>\d+)/(?P<ects_id>\d+)$',
        syllabus_my.syllabus_delete_ects,
        name='delete_ects'
    ),
    url(
        r'syllabus-module-show/(?P<syllabus_id>\d+)$',
        syllabus_my.syllabus_module_show,
        name='show_module'
    ),
    url(
        r'syllabus-module-edit/(?P<syllabus_id>\d+)$',
        syllabus_my.syllabus_module_edit,
        name='edit_module'
    ),
    url(
        r'syllabus-module-print/(?P<syllabus_id>\d+)$',
        syllabus_my.syllabus_module_print,
        name='print_module'
    ),
    url(
        r'syllabus-subject-show/(?P<syllabus_id>\d+)$',
        syllabus_my.syllabus_subject_show,
        name='show_subject'
    ),
    url(
        r'syllabus-subject-edit/(?P<syllabus_id>\d+)$',
        syllabus_my.syllabus_subject_edit,
        name='edit_subject'
    ),
    url(
        r'syllabus-subject-print/(?P<syllabus_id>\d+)$',
        syllabus_my.syllabus_subject_print,
        name='print_subject'
    ),

    url(
        r'syllabus-module-copy-list/(?P<syllabus_id>\d+)$',
        syllabus_my.syllabus_module_copy_list,
        name='module_copy_list'
    ),
    url(
        r'syllabus-module-copy/(?P<syllabus_to_id>\d+)/(?P<syllabus_from_id>\d+)$',
        syllabus_my.syllabus_module_copy,
        name='copy_module'
    ),
    url(
        r'syllabus-subject-copy-list/(?P<syllabus_id>\d+)$',
        syllabus_my.syllabus_subject_copy_list,
        name='subject_copy_list'
    ),
    url(
        r'syllabus-subject-copy/(?P<syllabus_to_id>\d+)/(?P<syllabus_from_id>\d+)$',
        syllabus_my.syllabus_subject_copy,
        name='copy_subject'
    ),
    
    url(
        r'syllabus-practice-show/(?P<syllabus_id>\d+)$',
        syllabus_my.syllabus_practice_show,
        name='show_practice'
    ),
    url(
        r'syllabus-practice-edit/(?P<syllabus_id>\d+)$',
        syllabus_my.syllabus_practice_edit,
        name='edit_practice'
    ),
    url(
        r'syllabus-practice-print/(?P<syllabus_id>\d+)$',
        syllabus_my.syllabus_practice_print,
        name='print_practice'
    ),
]

search_urlpatterns = [
    url(
        r'search-classic/$',
        search_engine.syllabus_search_classic,
        name='classic'
    ),
    url(
        r'show/(?P<syllabus_type>\d{1})/(?P<syllabus_id>\d+)$',
        search_engine.syllabus_show,
        name='show'
    ),
]

browser_urlpatterns = [
    url(
        r'^syllabus/select/(?P<course_id>\d+)$',
        browser.select_semester,
        name='select_semester'
    ),
    url(
        r'^syllabus/browse/(?P<course_id>\d+)/(?P<semester>\d+)$',
        browser.browse,
        name='browse'
    ),
    url(
        r'^syllabus/supervise/(?P<course_id>\d+)/(?P<semester>\d+)$',
        browser.supervise,
        name='supervise'
    ),
]


urlpatterns = [
    url(r'my/', include(my_urlpatterns, namespace='my')),
    url(r'search/', include(search_urlpatterns, namespace='search')),
    url(r'browse/', include(browser_urlpatterns, namespace='browser')),
    url(
        r'^confirm/(?P<syllabus_to_id>\d+)/(?P<syllabus_from_id>\d+)?$',
        metacortex.confirm,
        name='confirm'
    ),
    url(
        r'^confirm/sm/(?P<syllabus_to_id>\d+)/(?P<syllabus_from_id>\d+)?$',
        metacortex.confirm_sm,
        name='confirm_sm'
    ),
    url(
        r'^help$',
        metacortex.show_help,
        name='help'
    ),
]

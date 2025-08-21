import os

from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from apps.metacortex.forms.reform_2011.forms import SyllabusClassicSearchForm
from apps.metacortex.models import (SyllabusModule, SyllabusPractice,
                                    SyllabusSubject)
from apps.metacortex.settings import (SYLLABUS_TYPE_GENERAL_ID,
                                      SYLLABUS_TYPE_MODULE_ID,
                                      SYLLABUS_TYPE_PRACTICE_ID,
                                      SYLLABUS_TYPE_SUBJECT_ID)
from apps.metacortex.views.reform_2011.search_engine import syllabus_show_2011
from apps.metacortex.views.reform_2019.search_engine import syllabus_show_2019

TEMPLATE_ROOT = 'metacortex/search_engine/'


def syllabus_show(request, syllabus_type, syllabus_id):
    syllabus_type = int(syllabus_type)

    types = {
        SYLLABUS_TYPE_MODULE_ID: SyllabusModule.objects.details(),
        SYLLABUS_TYPE_SUBJECT_ID: SyllabusSubject.objects.details(syllabus_id)
    }
    try:
        model = types[syllabus_type]
    except KeyError:
        raise Http404("Nie istnieje sylabus o wybranym typie")

    syllabus = get_object_or_404(model, id=syllabus_id)

    if isinstance(syllabus, SyllabusModule):
        course = syllabus.module.get_course()
    else:
        course = syllabus.subject.module.get_course()

    if course.reform_2019():
        return syllabus_show_2019(request, syllabus)
    else:
        return syllabus_show_2011(request, syllabus)


# -----------------------------------------------------------------
# --- CLASSIC SYLLABUS SEARCH
# -----------------------------------------------------------------

def syllabus_search_classic(request):
    query = request.GET.get('q', '')
    syllabus_type = request.GET.get('syllabus_type', SYLLABUS_TYPE_SUBJECT_ID)
    syllabus_type = int(syllabus_type)

    form = SyllabusClassicSearchForm(request.GET)
    syllabusses_list = classic_search(query, syllabus_type)

    paginator = Paginator(syllabusses_list, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
        
    try:
        syllabusses = paginator.page(page)
    except (EmptyPage, InvalidPage):
        syllabusses = paginator.page(paginator.num_pages)    

    context = {
        'form': form,
        'syllabusses': syllabusses,
        'syllabus_type': syllabus_type
    }
    template_path = os.path.join(TEMPLATE_ROOT, 'search_classic.html')
    return render(request, template_path, context)


def classic_search(query, syllabus_type):
    q = query.split(',')
    syllabus_type = int(syllabus_type)

    types = {
        SYLLABUS_TYPE_MODULE_ID: module_classic_search_engine,
        SYLLABUS_TYPE_SUBJECT_ID: subject_classic_search_engine,
        SYLLABUS_TYPE_PRACTICE_ID: practice_classic_search_engine,
        SYLLABUS_TYPE_GENERAL_ID: general_classic_search_engine
    }

    search_function = types[syllabus_type]
    return search_function(q)


def module_classic_search_engine(q):
    queryset = SyllabusModule.objects.published().search()
    for key in q:
        queryset = queryset.filter(get_classic_module_query(key))
    return queryset


def subject_classic_search_engine(q):
    queryset = SyllabusSubject.objects.published().search()
    for key in q:
        queryset = queryset.filter(get_classic_subject_query(key))
    return queryset.order_by('subject__name', 'additional_name', 'teacher')


def practice_classic_search_engine(q):
    queryset = SyllabusPractice.objects.published().search()
    for key in q:
        queryset = queryset.filter(get_classic_practice_query(key))
    return queryset


def general_classic_search_engine(q):
    queryset = SyllabusSubject.objects.published().search().general()
    for key in q:
        queryset = queryset.filter(
            get_classic_general_query(key)
        )
    return queryset


def get_classic_module_query(key):
    key = key.strip()
    return Q(module__sgroup__course__department__name__istartswith=key) | \
        Q(module__sgroup__course__name__istartswith=key) | \
        Q(module__sgroup__course__name__istartswith=key) | \
        Q(module__sgroup__course__level__name__istartswith=key) | \
        Q(module__name__istartswith=key) | \
        Q(coordinator__user_profile__user__last_name__istartswith=key) | \
        Q(module__internal_code__istartswith=key)


def get_classic_subject_query(key):
    key = key.strip()
    return Q(subject__module__sgroup__course__department__name__istartswith=key) | \
        Q(subject__module__sgroup__course__name__istartswith=key) | \
        Q(subject__module__sgroup__course__level__name__istartswith=key) | \
        Q(subject__module__name__istartswith=key) | \
        Q(subject__name__istartswith=key) | \
        Q(additional_name__istartswith=key) | \
        Q(teacher__user_profile__user__last_name__istartswith=key) | \
        Q(subject__internal_code__istartswith=key)


def get_classic_practice_query(key):
    key = key.strip()
    return Q(subject__module__sgroup__course__department__name__istartswith=key) | \
        Q(subject__module__sgroup__course__name__istartswith=key) | \
        Q(subject__module__sgroup__course__level__name__istartswith=key) | \
        Q(subject__module__name__istartswith=key) | \
        Q(subject__name__istartswith=key) | \
        Q(teacher__user_profile__user__last_name__istartswith=key)


def get_classic_general_query(key):
    key = key.strip()
    return Q(subject__module__sgroup__course__department__name__istartswith=key) | \
        Q(subject__module__sgroup__course__name__istartswith=key) | \
        Q(subject__module__sgroup__course__level__name__istartswith=key) | \
        Q(subject__module__name__istartswith=key) | \
        Q(subject__name__istartswith=key) | \
        Q(additional_name__istartswith=key) | \
        Q(teacher__user_profile__user__last_name__istartswith=key) | \
        Q(subject__internal_code__istartswith=key)

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _

from apps.metacortex.forms.reform_2011.forms import SearchForm
from apps.metacortex.models import (ECTS, Syllabus, SyllabusModule,
                                    SyllabusPractice, SyllabusSubject,
                                    SyllabusToECTS)
from apps.metacortex.settings import (DEFAULT_SYLLABUS_SEMESTER,
                                      DEFAULT_SYLLABUS_TYPE,
                                      DEFAULT_SYLLABUS_YEAR,
                                      SUBJECT_TYPE_PRACTICE_ID)
from apps.metacortex.views.reform_2011.syllabus_module import (
    syllabus_module_edit_2011, syllabus_module_print_2011,
    syllabus_module_show_2011)
from apps.metacortex.views.reform_2011.syllabus_my import show_2011
from apps.metacortex.views.reform_2011.syllabus_practice import (
    syllabus_practice_edit_2011, syllabus_practice_print_2011,
    syllabus_practice_show_2011)
from apps.metacortex.views.reform_2011.syllabus_subject import (
    syllabus_subject_edit_2011, syllabus_subject_print_2011,
    syllabus_subject_show_2011)
from apps.metacortex.views.reform_2019.syllabus_module import (
    syllabus_module_edit_2019, syllabus_module_print_2019,
    syllabus_module_show_2019)
from apps.metacortex.views.reform_2019.syllabus_my import show_2019
from apps.metacortex.views.reform_2019.syllabus_subject import (
    syllabus_subject_edit_2019, syllabus_subject_print_2019,
    syllabus_subject_show_2019)
from apps.trainman.models import Teacher, UserProfile

TEMPLATE_ROOT = 'metacortex/syllabus_my/'


@login_required
def show(request):
    """ Wyświetla wszystkie sylabusy zalogowanego pracownika. """

    teacher = None
    try:
        teacher = request.user.userprofile.teacher
    except Teacher.DoesNotExist:
        messages.add_message(
            request,
            messages.ERROR,
            _(u'You do not have a teacher profile.')
        )
    except UserProfile.DoesNotExist:
        messages.add_message(
            request,
            messages.ERROR,
            _(u'You do not have a user profile.')
        )

    syllabus_year = int(request.GET.get('year', DEFAULT_SYLLABUS_YEAR))
    syllabus_semester = int(request.GET.get('semester', DEFAULT_SYLLABUS_SEMESTER))
    syllabus_type = int(request.GET.get('type', DEFAULT_SYLLABUS_TYPE))

    if syllabus_year >= 2019:
        return show_2019(request, teacher, syllabus_year, syllabus_semester,
                         syllabus_type)
    else:
        return show_2011(request, teacher, syllabus_year, syllabus_semester,
                         syllabus_type)


# -----------------------------------------------------------------
# --- SYLLABUS MODULE
# -----------------------------------------------------------------

@login_required
def syllabus_module_edit(request, syllabus_id):
    syllabus = get_object_or_404(SyllabusModule, id=syllabus_id)
    course = syllabus.module.get_course()

    if course.reform_2019():
        return syllabus_module_edit_2019(request, syllabus)
    else:
        return syllabus_module_edit_2011(request, syllabus)


@login_required
def syllabus_module_show(request, syllabus_id):
    syllabus = get_object_or_404(SyllabusModule, id=syllabus_id)
    course = syllabus.module.get_course()

    if course.reform_2019():
        return syllabus_module_show_2019(request, syllabus)
    else:
        return syllabus_module_show_2011(request, syllabus)


def syllabus_module_print(request, syllabus_id):
    syllabus = get_object_or_404(SyllabusModule, id=syllabus_id)
    course = syllabus.module.get_course()

    if course.reform_2019():
        return syllabus_module_print_2019(request, syllabus)
    else:
        return syllabus_module_print_2011(request, syllabus)


# -----------------------------------------------------------------
# --- SYLLABUS PRACTICE
# -----------------------------------------------------------------

@login_required
def syllabus_practice_edit(request, syllabus_id):
    syllabus = get_object_or_404(SyllabusPractice, id=syllabus_id)
    return syllabus_practice_edit_2011(request, syllabus)


@login_required
def syllabus_practice_show(request, syllabus_id):
    syllabus = get_object_or_404(SyllabusPractice, id=syllabus_id)
    return syllabus_practice_show_2011(request, syllabus)


def syllabus_practice_print(request, syllabus_id):
    syllabus = get_object_or_404(SyllabusPractice, id=syllabus_id)
    return syllabus_practice_print_2011(request, syllabus)


# -----------------------------------------------------------------
# --- SYLLABUS SUBJECT
# -----------------------------------------------------------------

@login_required
def syllabus_subject_edit(request, syllabus_id):
    syllabus = get_object_or_404(SyllabusSubject, id=syllabus_id)
    course = syllabus.subject.module.get_course()

    if course.reform_2019():
        return syllabus_subject_edit_2019(request, syllabus)
    else:
        return syllabus_subject_edit_2011(request, syllabus)


@login_required
def syllabus_subject_show(request, syllabus_id):
    syllabus = get_object_or_404(SyllabusSubject, id=syllabus_id)
    course = syllabus.subject.module.get_course()

    if course.reform_2019():
        return syllabus_subject_show_2019(request, syllabus)
    else:
        return syllabus_subject_show_2011(request, syllabus)


def syllabus_subject_print(request, syllabus_id):
    syllabus = get_object_or_404(SyllabusSubject, id=syllabus_id)
    course = syllabus.subject.module.get_course()

    if course.reform_2019():
        return syllabus_subject_print_2019(request, syllabus)
    else:
        return syllabus_subject_print_2011(request, syllabus)


# -----------------------------------------------------------------
# --- ECTS
# -----------------------------------------------------------------

@login_required
@transaction.atomic
def syllabus_delete_ects(request, syllabus_type, syllabus_id, ects_id):
    try:
        ects = ECTS.objects.get(id=ects_id)
        ects.delete()
        messages.success(request, _(u'ECTS equivalen has been successfully deleted'))
    except Syllabus.DoesNotExist:
        messages.error(request, _(u'En error occured while deleting ECTS equivalent'))
    except ECTS.DoesNotExist:
        messages.error(request, _(u'En error occured while deleting ECTS equivalent'))
    except SyllabusToECTS.MultipleObjectsReturned:
        messages.error(request, _(u'En error occured while deleting ECTS equivalent'))

    if int(syllabus_type) == SUBJECT_TYPE_PRACTICE_ID:
        return redirect('metacortex:my:edit_practice', syllabus_id=syllabus_id)
    return redirect('metacortex:my:edit_subject', syllabus_id=syllabus_id)


# -----------------------------------------------------------------
# --- SYLLABUS SUBJECT COPY
# -----------------------------------------------------------------

def syllabus_subject_copy_list(request, syllabus_id):
    # Formularz wyszukiwania
    name = request.session.get('syllabus_copy_search_name', '')
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            name = request.session['syllabus_copy_search_name'] = search_form.cleaned_data['name']
    else:
        search_form = SearchForm(initial={'name': name})
    
    # Pobranie sylabusów spełniających kryteria
    syllabus = get_object_or_404(SyllabusSubject, id=syllabus_id)
    syllabusses_list = SyllabusSubject.objects.published().filter(
        Q(additional_name__istartswith=name) |
        Q(subject__name__istartswith=name) |
        Q(teacher__user_profile__user__last_name__istartswith=name)
    )
    
    # Paginacja
    paginator = Paginator(syllabusses_list, 15)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
        
    try:
        syllabusses = paginator.page(page)
    except (EmptyPage, InvalidPage):
        syllabusses = paginator.page(paginator.num_pages)
    
    kwargs = {
        'syllabus': syllabus,
        'syllabusses': syllabusses,
        'search_form': search_form
    }
    return render(request, TEMPLATE_ROOT+'syllabus_subject_copy_list.html', kwargs)


def syllabus_subject_copy(request, syllabus_to_id, syllabus_from_id):
    syllabus_to = get_object_or_404(SyllabusSubject, id=syllabus_to_id)
    syllabus_from = get_object_or_404(SyllabusSubject, id=syllabus_from_id)
    
    try:
        syllabus_to.is_published = syllabus_from.is_published
        syllabus_to.additional_name = syllabus_from.additional_name
        syllabus_to.initial_requirements = syllabus_from.initial_requirements
        syllabus_to.subjects_scope = syllabus_from.subjects_scope
        syllabus_to.assessment_conditions = syllabus_from.assessment_conditions
        syllabus_to.literature = syllabus_from.literature
        syllabus_to.additional_information = syllabus_from.additional_information
        syllabus_to.education_effects = syllabus_from.education_effects
        syllabus_to.learning_outcomes_verification = syllabus_from.learning_outcomes_verification

        if syllabus_to.subject.module.get_course().start_date.year == 2019:
            # New type of learning outcomes was introduced in 2019. Module learning
            # outcomes should not be copied from previous year.
            pass
        else:
            syllabus_to.module_learning_outcomes = syllabus_from.module_learning_outcomes.all()

        syllabus_to.save()
        
        syllabus_to.assessment_forms.clear()
        for assessment_form in syllabus_from.assessment_forms.all():
            syllabus_to.assessment_forms.add(assessment_form)
            
        syllabus_to.didactic_methods.clear()
        for didactic_method in syllabus_from.didactic_methods.all():
            syllabus_to.didactic_methods.add(didactic_method)

        syllabus_to.ectss.clear()
        for syllabus_to_ects in SyllabusToECTS.objects.filter(syllabus=syllabus_from):
            syllabus_to_ects.id = None
            syllabus_to_ects.syllabus = syllabus_to
            syllabus_to_ects.save()
    except:
        messages.error(request, _(u'En error occured while copying syllabus'))
    else:
        messages.success(request, _(u'Syllabus has been successfully copied'))
    
    return redirect('metacortex:my:show')


# -----------------------------------------------------------------
# --- SYLLABUS MODULE COPY
# -----------------------------------------------------------------

def syllabus_module_copy_list(request, syllabus_id):
    # Formularz wyszukiwania
    name = request.session.get('syllabus_copy_search_name', '')
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            name = request.session['syllabus_copy_search_name'] = search_form.cleaned_data['name']
    else:
        search_form = SearchForm(initial={'name': name})

    # Pobranie sylabusów spełniających kryteria
    syllabus = get_object_or_404(SyllabusModule, id=syllabus_id)
    syllabusses_list = SyllabusModule.objects.published().filter(
        Q(module__name__istartswith=name) |
        Q(module__coordinator__user_profile__user__last_name__istartswith=name)
    )

    # Paginacja
    paginator = Paginator(syllabusses_list, 15)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        syllabusses = paginator.page(page)
    except (EmptyPage, InvalidPage):
        syllabusses = paginator.page(paginator.num_pages)

    kwargs = {
        'syllabus': syllabus,
        'syllabusses': syllabusses,
        'search_form': search_form
    }
    return render(request, TEMPLATE_ROOT+'syllabus_module_copy_list.html', kwargs)


def syllabus_module_copy(request, syllabus_to_id, syllabus_from_id):
    syllabus_to = get_object_or_404(SyllabusModule, id=syllabus_to_id)
    syllabus_from = get_object_or_404(SyllabusModule, id=syllabus_from_id)

    try:
        syllabus_to.is_published = syllabus_from.is_published
        syllabus_to.module_description = syllabus_from.module_description
        syllabus_to.lecture_languages = syllabus_from.lecture_languages.all()
        syllabus_to.unit_source = syllabus_from.unit_source
        syllabus_to.unit_target = syllabus_from.unit_target
        syllabus_to.additional_information = syllabus_from.additional_information
        syllabus_to.save()
    except:
        messages.error(request, _(u'En error occured while copying syllabus'))
    else:
        messages.success(request, _(u'Syllabus has been successfully copied'))

    return redirect('metacortex:my:show')


# -----------------------------------------------------------------
# --- SYLLABUS COPYING
# -----------------------------------------------------------------

def copy_module_syllabus_data(syllabus_from, syllabus_to):
    syllabus_to.is_published = syllabus_from.is_published
    syllabus_to.module_description = syllabus_from.module_description
    syllabus_to.lecture_languages = syllabus_from.lecture_languages.all()
    syllabus_to.unit_source = syllabus_from.unit_source
    syllabus_to.unit_target = syllabus_from.unit_target
    syllabus_to.coordinator = syllabus_from.coordinator
    syllabus_to.additional_information = syllabus_from.additional_information
    syllabus_to.save()


def copy_subject_syllabus_data(syllabus_from, syllabus_to):
    syllabus_to.is_published = syllabus_from.is_published
    syllabus_to.additional_name = syllabus_from.additional_name
    syllabus_to.initial_requirements = syllabus_from.initial_requirements
    syllabus_to.subjects_scope = syllabus_from.subjects_scope
    syllabus_to.assessment_conditions = syllabus_from.assessment_conditions
    syllabus_to.module_learning_outcomes = syllabus_from.module_learning_outcomes.all()
    syllabus_to.literature = syllabus_from.literature
    syllabus_to.additional_information = syllabus_from.additional_information
    syllabus_to.education_effects = syllabus_from.education_effects
    syllabus_to.save()
    
    syllabus_to.assessment_forms.clear()
    syllabus_to.assessment_forms = syllabus_from.assessment_forms.all()    
    syllabus_to.didactic_methods.clear()
    syllabus_to.didactic_methods = syllabus_from.didactic_methods.all()
    
    copy_ects_equivalents_data(syllabus_from, syllabus_to)


def copy_practice_syllabus_data(syllabus_from, syllabus_to):
    syllabus_to.is_published = syllabus_from.is_published
    syllabus_to.teacher = syllabus_from.teacher
    syllabus_to.type = syllabus_from.type
    syllabus_to.description = syllabus_from.description
    syllabus_to.education_effects = syllabus_from.education_effects
    syllabus_to.additional_information = syllabus_from.additional_information
    syllabus_to.save()
    
    copy_ects_equivalents_data(syllabus_from, syllabus_to)


def copy_ects_equivalents_data(syllabus_from, syllabus_to):
    syllabus_to.ectss.clear()
    for equivalent in syllabus_from.get_equivalents():
        syllabus_to_ects = SyllabusToECTS()
        syllabus_to_ects.ects = equivalent.ects
        syllabus_to_ects.syllabus = syllabus_to
        syllabus_to_ects.hours = equivalent.hours
        syllabus_to_ects.save()

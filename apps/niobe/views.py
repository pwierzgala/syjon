# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _

from apps.merovingian.functions import make_page, user_courses, user_subjects
from apps.merovingian.models import (
    Course, MerovingianAdmin, Module, Subject, SubjectToTeacher)
from apps.niobe.forms import (
    CoordinatorForm, SearchForm, SubjectToTeacherInlineFormset)
from apps.trainman.models import Teacher


def user_course_subjects(user, module):
    try:
        admin = MerovingianAdmin.objects.get(user_profile__user=user)
    except MerovingianAdmin.DoesNotExist:
        admin = None

    if user.is_superuser or (admin is not None and admin.temporary_privileged_access):
        subjects = Subject.objects.all()
    else:
        subjects = Subject.objects.didactic_offer_and_future()

    return subjects.filter(module=module)


@login_required
def index(request):
    # Getting courses matching criteria
    courses = user_courses(request.user)

    # Search form
    name = ''
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            name = request.session['niobe_courses_search'] = search_form.cleaned_data['name']
    else:
        name = request.session.get('niobe_courses_search', '')
        search_form = SearchForm(initial={'name': name})
    if name != '':
        courses = courses.filter(name__istartswith=name)

    # Pagination
    paginator = Paginator(courses, 25)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        courses = paginator.page(page)
    except (EmptyPage, InvalidPage):
        courses = paginator.page(paginator.num_pages)

    kwargs = {'courses': courses, 'search_form': search_form}
    return render(request, 'niobe/index.html', kwargs)


@login_required
def course_modules(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    modules = Module.objects.course(course)

    context = {
        'course': course,
        'modules': modules
    }
    return render(request, 'niobe/course_modules.html', context)


@login_required
def course_subjects(request, course_id, module_id):
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)
    subjects = user_course_subjects(request.user, module)

    if request.method == 'POST':
        form = CoordinatorForm(request.POST, instance=module)
        if form.is_valid():
            if form.cleaned_data['delete']:
                module.coordinator = None
                module.save()
            else:
                form.save()
            messages.success(request, u'Formularz został pomyślnie zapisany')
            return redirect('niobe:subject-list', course_id=course.id, module_id=module.id)
    else:
        form = CoordinatorForm(instance=module)

    subject_teacher = [
        {
            'subject': subject,
            'subject_to_teacher': SubjectToTeacher.objects.filter(subject=subject).order_by('teacher__user_profile__user__last_name')
        } 
        for subject in subjects
    ]
    
    kwargs = {
        'course': course,
        'module': module,
        'subjects': subject_teacher,
        'form': form
    }
    return render(request, 'niobe/course_subjects.html', kwargs)


@login_required
@permission_required('merovingian.change_subject')
def subject_show(request, course_id, module_id, subject_id):
    # todo: dodaj sprawdzanie czy użytkownik ma uprawnienia do tego przedmiotu.
    # todo: dodaj sprawdzanie czy nauczyciel jest wymieniony na liście jednoktornie.
    # todo: sprawdź czy istnieją sytuacje, że są dwa sylabusy modułu do jednego modułu.
    # todo: sprawadź czy istnieją moduły, które nie należą do żadnej specjalności.
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == 'POST':
        subject_to_teacher_formset = SubjectToTeacherInlineFormset(request.POST, request.FILES, instance=subject)
        if subject_to_teacher_formset.is_valid():
            subject_to_teacher_formset.save()
            messages.success(request, _(u'Subject %s has been saved succesfully.') % subject)

            if request.POST.get('action') == 'save':
                return redirect('niobe:subject-list', course_id=course.id, module_id=module.id)
            elif request.POST.get('action') == 'save_and_edit':
                return redirect('niobe:subject-details', course_id=course.id, module_id=module.id, subject_id=subject.id)
        else:
            messages.error(request, _(u'Correct errors listed below.'))
    else:
        subject_to_teacher_formset = SubjectToTeacherInlineFormset(instance=subject)

    kwargs = {
        'course': course,
        'module': module,
        'subject': subject,
        'subject_to_teacher_formset': subject_to_teacher_formset
    }
    return render(request, 'niobe/subject_show.html', kwargs)


# --- Teachers ---

@login_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            name = search_form.cleaned_data['name']
            teachers = teachers.filter(user_profile__user__last_name__istartswith = name, user_profile__user__is_active=True)
    else:
        search_form = SearchForm()

    kwargs = {
        'teachers_page': make_page(request, teachers),
        'search_form': search_form
    }
    return render(request, 'niobe/teacher_list.html', kwargs)

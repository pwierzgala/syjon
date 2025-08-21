import os

from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy as _

from apps.syjon.lib.pdf import render_to_pdf
from apps.trinity.forms import CourseLearningOutcomeForm
from apps.trinity.models import CourseLearningOutcome
from apps.trinity.views.trinity import (get_alos_for_course,
                                        is_learning_outcomes_administrator)

TEMPLATE_ROOT = 'trinity/clo/reform_2011'


def show_2011(request, course, education_category):
    clos = CourseLearningOutcome.objects.filter(
        course=course,
        education_category=education_category
    ).prefetch_related('alos')

    is_course_admin = is_learning_outcomes_administrator(request.user, course)

    context = {
        'course': course,
        'education_category': education_category,
        'clos': clos,
        'is_course_admin': is_course_admin
    }

    if course.is_level_ba() or course.is_level_msc() or course.is_level_u_msc() or course.is_level_eng():
        alos = get_alos_for_course(course, education_category)
        context['remaining_alos'] = alos.exclude(clos__in=clos)

    template_path = os.path.join(TEMPLATE_ROOT, 'show.html')
    return render(request, template_path, context)


def add_2011(request, course, education_category):
    queryset = get_alos_for_course(course, education_category)
    initial = {
        'course': course,
        'education_category': education_category
    }
    form = CourseLearningOutcomeForm(
        request.POST or None,
        queryset=queryset,
        initial=initial
    )

    if request.method == 'POST':
        if form.is_valid(): 
            form.save()
            messages.success(request, _(u'Changes have been successfully saved'))
            if 'save' in request.POST:
                return redirect(
                    'trinity:clo:show',
                    course_id=course.id,
                    education_category_id=education_category.id
                )
            else:
                return redirect(
                    'trinity:clo:add',
                    course_id=course.id,
                    education_category_id=education_category.id
                )
    
    context = {
        'form': form,
        'course': course,
        'education_category': education_category
    }
    template_path = os.path.join(TEMPLATE_ROOT, "add_update.html")
    return render(request, template_path, context)


def update_2011(request, course, education_category, clo):
    queryset = get_alos_for_course(course, education_category)
    form = CourseLearningOutcomeForm(
        request.POST or None,
        queryset=queryset,
        instance=clo
    )
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, _(u'Changes have been successfully saved'))
            return redirect(
                'trinity:clo:show',
                course_id=course.id,
                education_category_id=education_category.id
            )
    
    kwargs = {
        'form': form,
        'course': course,
        'education_category': education_category,
        'edit': True
    }
    template_path = os.path.join(TEMPLATE_ROOT, "add_update.html")
    return render(request, template_path, kwargs)


def print_pdf_2011(request, course):
    clos = CourseLearningOutcome.objects.filter(course=course)
    template_path = os.path.join(TEMPLATE_ROOT, 'print.html')
    template_context = {'course': course, 'clos': clos}
    pdf_file_name = 'output'
    return render_to_pdf(request, template_path, template_context, pdf_file_name)

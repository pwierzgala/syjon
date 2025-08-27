import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _

from apps.merovingian.models import Course
from apps.trinity.models import CourseLearningOutcome, EducationCategory
from apps.trinity.views.reform_2011.clo import (add_2011, print_pdf_2011,
                                                show_2011, update_2011)
from apps.trinity.views.reform_2019.clo import (add_2019, print_pdf_2019,
                                                show_2019, update_2019)
from apps.trinity.views.trinity import trinity_administrator_required

TEMPLATE_ROOT = 'trinity/clo/'


def education_category_select(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    education_categories = EducationCategory.objects.all()
    context = {
        'education_categories': education_categories,
        'course': course
    }
    template_path = os.path.join(TEMPLATE_ROOT, 'select_category.html')
    return render(request, template_path, context)


def show(request, course_id, education_category_id):
    course = get_object_or_404(Course, pk=course_id)
    education_category = get_object_or_404(EducationCategory, pk=education_category_id)

    if course.reform_2019():
        return show_2019(request, course, education_category)
    else:
        return show_2011(request, course, education_category)


@login_required
@trinity_administrator_required
def add(request, course_id, education_category_id):
    course = get_object_or_404(Course, pk=course_id)
    education_category = get_object_or_404(EducationCategory, pk=education_category_id)

    if course.reform_2019():
        return add_2019(request, course, education_category)
    else:
        return add_2011(request, course, education_category)


@login_required
@trinity_administrator_required
def update(request, course_id, education_category_id, clo_id):
    course = get_object_or_404(Course, pk=course_id)
    education_category = get_object_or_404(EducationCategory, pk=education_category_id)
    clo = CourseLearningOutcome.objects.get(id=clo_id)

    if course.reform_2019():
        return update_2019(request, course, education_category, clo)
    else:
        return update_2011(request, course, education_category, clo)


@login_required
@trinity_administrator_required
def delete(request, course_id, education_category_id):
    course = get_object_or_404(Course, pk=course_id)
    education_category = get_object_or_404(EducationCategory, pk=education_category_id)

    if request.method == 'POST':
        clo_ids = request.POST.getlist('selected_id')
        clos = CourseLearningOutcome.objects.filter(id__in=clo_ids)
        clos.delete()
        messages.success(request, _(u'Selected objects were deleted.'))

    return redirect(
        'trinity:clo:show',
        course_id=course.id,
        education_category_id=education_category.id
    )


def print_pdf(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if course.reform_2019():
        return print_pdf_2019(request, course)
    else:
        return print_pdf_2011(request, course)

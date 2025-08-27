# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _

from apps.merovingian.models import Course
from apps.trinity.forms import EducationAreaForm, EducationAreaPhdForm
from apps.trinity.views.trinity import trinity_administrator_required

TEMPLATE_ROOT = 'trinity/ea/'

@login_required
@trinity_administrator_required
def assign(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if course.is_level_phd():
        messages.error(request, 'Nie masz uprawnień do przeglądania tej strony.')
        return redirect('merovingian:course:details', course_id=course.id)

    form = EducationAreaForm(request.POST or None, instance=course)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, _(u'Changes have been successfully saved'))
            return redirect('trinity:ea:assign', course_id=course.id)

    context = {'course': course, 'form': form}
    return render(request, TEMPLATE_ROOT + 'assign.html', context)


@login_required
@trinity_administrator_required
def assign_phd(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    form = EducationAreaPhdForm(request.POST or None, instance=course)

    if not course.is_level_phd():
        messages.error(request, 'Nie masz uprawnień do przeglądania tej strony.')
        return redirect('merovingian:course:details', course_id=course.id)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, _(u'Changes have been successfully saved'))
            return redirect('trinity:ea:assign_phd', course_id=course.id)

    context = {'course': course, 'form': form}
    return render(request, TEMPLATE_ROOT + 'assign_phd.html', context)

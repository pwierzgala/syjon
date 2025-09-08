import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.merovingian.models import Course, Module, SGroup
from apps.trinity.models import ModuleLearningOutcome
from apps.trinity.views.reform_2011.mlo import (
    add_2011, print_pdf_2011, select_module_2011, show_2011, update_2011)
from apps.trinity.views.reform_2019.mlo import (
    add_2019, print_pdf_2019, select_module_2019, show_2019, update_2019)
from apps.trinity.views.trinity import trinity_administrator_required

TEMPLATE_ROOT = 'trinity/mlo/'


def select_sgroup(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    sgroups = SGroup.objects.active().filter(course=course)
    context = {
        'sgroups': sgroups,
        'course': course
    }
    template_path = os.path.join(TEMPLATE_ROOT, 'select_sgroup.html')
    return render(request, template_path, context)


def select_module(request, course_id, sgroup_id):
    course = get_object_or_404(Course, pk=course_id)
    sgroup = get_object_or_404(SGroup, pk=sgroup_id)

    if course.reform_2019():
        return select_module_2019(request, course, sgroup)
    else:
        return select_module_2011(request, course, sgroup)


def show(request, course_id, sgroup_id, module_id):
    course = get_object_or_404(Course, pk=course_id)
    sgroup = get_object_or_404(SGroup, pk=sgroup_id)
    module = get_object_or_404(Module, pk=module_id)

    if course.reform_2019():
        return show_2019(request, course, sgroup, module)
    else:
        return show_2011(request, course, sgroup, module)


@login_required
@trinity_administrator_required
def add(request, course_id, sgroup_id, module_id):
    course = get_object_or_404(Course, pk=course_id)
    sgroup = get_object_or_404(SGroup, pk=sgroup_id)
    module = get_object_or_404(Module, pk=module_id)

    if course.reform_2019():
        return add_2019(request, course, sgroup, module)
    else:
        return add_2011(request, course, sgroup, module)


@login_required
@trinity_administrator_required
def update(request, course_id, sgroup_id, module_id, mlo_id):
    course = get_object_or_404(Course, pk=course_id)
    sgroup = get_object_or_404(SGroup, pk=sgroup_id)
    module = get_object_or_404(Module, pk=module_id)
    mlo = ModuleLearningOutcome.objects.get(id=mlo_id)

    if course.reform_2019():
        return update_2019(request, course, sgroup, module, mlo)
    else:
        return update_2011(request, course, sgroup, module, mlo)


@login_required
@trinity_administrator_required
def delete(request, course_id, sgroup_id, module_id):
    course = get_object_or_404(Course, pk=course_id)
    sgroup = get_object_or_404(SGroup, pk=sgroup_id)
    module = get_object_or_404(Module, pk=module_id)

    if request.method == 'POST':
        mlo_ids = request.POST.getlist('selected_id')
        mlos = ModuleLearningOutcome.objects.filter(id__in=mlo_ids)
        mlos.delete()
        messages.success(request, "Wybrane wiersze zostały usunięte")

    return redirect(
        'trinity:mlo:show',
        course_id=course.id,
        sgroup_id=sgroup.id,
        module_id=module.id
    )


def print_pdf(request, course_id, sgroup_id, module_id):
    course = get_object_or_404(Course, pk=course_id)
    sgroup = get_object_or_404(SGroup, pk=sgroup_id)
    module = get_object_or_404(Module, pk=module_id)

    if course.reform_2019():
        return print_pdf_2019(request, course, sgroup, module)
    else:
        return print_pdf_2011(request, course, sgroup, module)

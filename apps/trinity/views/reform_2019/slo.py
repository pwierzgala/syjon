import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.merovingian.models import Course, Module, SGroup, Subject
from apps.trinity.forms import SubjectLearningOutcomesForm
from apps.trinity.models import (ModuleLearningOutcome,
                                 SubjectToModuleLearningOutcome)
from apps.trinity.views.trinity import (is_learning_outcomes_administrator,
                                        trinity_administrator_required)

TEMPLATE_ROOT = 'trinity/slo/'


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
    modules = Module.objects.active().filter(sgroup=sgroup)
    context = {
        'modules': modules,
        'course': course,
        'sgroup': sgroup
    }
    template_path = os.path.join(TEMPLATE_ROOT, 'select_module.html')
    return render(request, template_path, context)


def select_subject(request, course_id, sgroup_id, module_id):
    course = get_object_or_404(Course, pk=course_id)
    sgroup = get_object_or_404(SGroup, pk=sgroup_id)
    module = get_object_or_404(Module, pk=module_id)
    subjects = Subject.objects.active().filter(module=module)
    context = {
        'subjects': subjects,
        'module': module,
        'course': course,
        'sgroup': sgroup
    }
    template_path = os.path.join(TEMPLATE_ROOT, 'select_subject.html')
    return render(request, template_path, context)


def show(request, course_id, sgroup_id, module_id, subject_id):
    course = get_object_or_404(Course, pk=course_id)
    sgroup = get_object_or_404(SGroup, pk=sgroup_id)
    module = get_object_or_404(Module, pk=module_id)
    subject = get_object_or_404(Subject, pk=subject_id)
    is_course_admin = is_learning_outcomes_administrator(request.user, course)

    context = {
        'course': course,
        'sgroup': sgroup,
        'module': module,
        'subject': subject,
        'is_course_admin': is_course_admin
    }
    template_path = os.path.join(TEMPLATE_ROOT, 'show.html')
    return render(request, template_path, context)


@login_required
@trinity_administrator_required
def update(request, course_id, sgroup_id, module_id, subject_id):
    course = get_object_or_404(Course, pk=course_id)
    sgroup = get_object_or_404(SGroup, pk=sgroup_id)
    module = get_object_or_404(Module, pk=module_id)
    subject = get_object_or_404(Subject, pk=subject_id)

    is_course_admin = is_learning_outcomes_administrator(request.user, course)
    mlos = ModuleLearningOutcome.objects.filter(module=module).prefetch_related('clos')

    initial_mlos = subject.slos.all()
    form = SubjectLearningOutcomesForm(
        request.POST or None,
        queryset=mlos,
        initial={"mlos": initial_mlos}
    )

    if request.method == 'POST':
        if form.is_valid():
            selected_mlos = form.cleaned_data["mlos"].all()

            # Add.
            mlos_to_create = set(selected_mlos).difference(set(initial_mlos))
            for mlo in mlos_to_create:
                SubjectToModuleLearningOutcome.objects.create(
                    subject=subject,
                    mlo=mlo
                )

            # Remove.
            mlos_to_remove = set(initial_mlos).difference(selected_mlos)
            for mlo in mlos_to_remove:
                subject_to_mlo = SubjectToModuleLearningOutcome.objects.get(
                    subject=subject,
                    mlo=mlo
                )
                subject_to_mlo.delete()

            messages.success(request, "Zmiany zostały zapisane")

            # Redirect.
            if 'save' in request.POST:
                return redirect(
                    'trinity:slo:show',
                    course_id=course.id,
                    sgroup_id=sgroup_id,
                    module_id=module_id,
                    subject_id=subject.id
                )
            else:
                return redirect(
                    'trinity:slo:update',
                    course_id=course.id,
                    sgroup_id=sgroup_id,
                    module_id=module_id,
                    subject_id=subject.id
                )

    context = {
        'mlos': mlos,
        'course': course,
        'sgroup': sgroup,
        'module': module,
        'subject': subject,
        'form': form,
        'is_course_admin': is_course_admin
    }
    template_path = os.path.join(TEMPLATE_ROOT, 'update.html')
    return render(request, template_path, context)

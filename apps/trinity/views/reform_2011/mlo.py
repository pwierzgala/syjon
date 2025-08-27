import os

from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from apps.merovingian.models import Module
from apps.syjon.lib.pdf import render_to_pdf
from apps.trinity.forms import ModuleLearningOutcomeForm
from apps.trinity.models import CourseLearningOutcome, ModuleLearningOutcome
from apps.trinity.views.trinity import is_learning_outcomes_administrator

TEMPLATE_ROOT = 'trinity/mlo/reform_2011/'


def select_module_2011(request, course, sgroup):
    modules = Module.objects.active().filter(sgroup=sgroup)
    context = {
        'modules': modules,
        'course': course,
        'sgroup': sgroup
    }
    template_path = os.path.join(TEMPLATE_ROOT, 'select_module.html')
    return render(request, template_path, context)


def show_2011(request, course, sgroup, module):
    is_course_admin = is_learning_outcomes_administrator(request.user, course)
    mlos = ModuleLearningOutcome.objects.filter(module=module).prefetch_related('clos')
    context = {
        'mlos': mlos,
        'course': course,
        'sgroup': sgroup,
        'module': module,
        'is_course_admin': is_course_admin
    }
    template_path = os.path.join(TEMPLATE_ROOT, 'show.html')
    return render(request, template_path, context)


def add_2011(request, course, sgroup, module):
    course_learning_outcomes = CourseLearningOutcome.objects.filter(course=course)
    initial = {'module': module}
    form = ModuleLearningOutcomeForm(
        request.POST or None,
        queryset=course_learning_outcomes,
        initial=initial
    )
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, _(u'Changes have been successfully saved'))
            if 'save' in request.POST:
                return redirect(
                    'trinity:mlo:show',
                    course_id=course.id,
                    sgroup_id=sgroup.id,
                    module_id=module.id
                )
            else:
                return redirect(
                    'trinity:mlo:add',
                    course_id=course.id,
                    sgroup_id=sgroup.id,
                    module_id=module.id
                )
    
    kwargs = {
        'form': form,
        'course': course,
        'sgroup': sgroup,
        'module': module
    }
    template_path = os.path.join(TEMPLATE_ROOT, 'add_update.html')
    return render(request, template_path, kwargs)


def update_2011(request, course, sgroup, module, mlo):
    course_learning_outcomes = CourseLearningOutcome.objects.filter(course=course)
    form = ModuleLearningOutcomeForm(
        request.POST or None,
        queryset=course_learning_outcomes,
        instance=mlo
    )

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, _(u'Changes have been successfully saved'))
            return redirect(
                'trinity:mlo:show',
                course_id=course.id,
                sgroup_id=sgroup.id,
                module_id=module.id
            )

    kwargs = {
        'form': form,
        'course': course,
        'sgroup': sgroup,
        'module': module,
        'edit': True
    }
    template_path = os.path.join(TEMPLATE_ROOT, 'add_update.html')
    return render(request, template_path, kwargs)


def print_pdf_2011(request, course, sgroup, module):
    mlos = ModuleLearningOutcome.objects.filter(module=module)

    template_path = os.path.join(TEMPLATE_ROOT, 'print.html')
    template_context = {
        'course': course,
        'sgroup': sgroup,
        'module': module,
        'mlos': mlos
    }
    pdf_file_name = 'output'
    return render_to_pdf(request, template_path, template_context, pdf_file_name)

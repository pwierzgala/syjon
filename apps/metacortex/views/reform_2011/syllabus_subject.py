import os

from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from apps.metacortex.forms.reform_2011.forms import SyllabusSubjectForm
from apps.metacortex.views.metacortex import save_ects
from apps.syjon.lib.functions import utf2ascii
from apps.syjon.lib.pdf import render_to_pdf
from apps.trinity.models import ModuleLearningOutcome

TEMPLATE_ROOT = 'metacortex/syllabus_my/reform_2011/subject/'


def syllabus_subject_edit_2011(request, syllabus):
    module_learning_outcomes = ModuleLearningOutcome.objects.filter(
        module=syllabus.subject.module
    )
    form = SyllabusSubjectForm(
        request.POST or None,
        instance=syllabus,
        module_learning_outcomes=module_learning_outcomes
    )

    if request.method == "POST":
        if form.is_valid():
            syllabus_subject = form.save(commit=False)
            syllabus_subject.save()

            syllabus_subject.didactic_methods = form.cleaned_data['didactic_methods']
            syllabus_subject.assessment_forms = form.cleaned_data['assessment_forms']
            syllabus_subject.module_learning_outcomes = form.cleaned_data['module_learning_outcomes']

            save_ects(syllabus_subject, request)

            messages.success(request, _(u'Syllabus has been successfully saved.'))
                
            if 'save' in request.POST:
                return redirect('metacortex:my:show')
            else:
                return redirect(
                    'metacortex:my:edit_subject',
                    syllabus_id=syllabus.id
                )
        else:
            messages.error(request, _(u'En error occured while saving syllabus.'))

    context = {
        'form': form,
        'syllabus': syllabus
    }
    template_path = os.path.join(TEMPLATE_ROOT, 'edit.html')
    return render(request, template_path, context)


def syllabus_subject_show_2011(request, syllabus):
    context = {'syllabus': syllabus}
    template_path = os.path.join(TEMPLATE_ROOT, 'show.html')
    return render(request, template_path, context)


def syllabus_subject_print_2011(request, syllabus):
    template_path = os.path.join(TEMPLATE_ROOT, 'print.html')
    file_name = utf2ascii('{code} {name}'.format(
        code=syllabus.subject.internal_code,
        name=syllabus.subject.name
    ))
    template_context = {'syllabus': syllabus}
    return render_to_pdf(request, template_path, template_context, file_name)

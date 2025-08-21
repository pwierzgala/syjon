import os

from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _

from apps.metacortex.forms.reform_2011.forms import SyllabusPracticeForm
from apps.syjon.lib.functions import utf2ascii
from apps.syjon.lib.pdf import render_to_pdf

TEMPLATE_ROOT = 'metacortex/syllabus_my/reform_2011/practice/'


def syllabus_practice_edit_2011(request, syllabus):
    form = SyllabusPracticeForm(request.POST or None, instance=syllabus)
    if request.method == "POST":
        if form.is_valid():
            syllabus_practice = form.save(commit=False)
            syllabus_practice.save()
            messages.success(request, _(u'Syllabus has been successfully saved.'))

            if 'save' in request.POST:
                return redirect('metacortex:my:show')
            else:
                return redirect(
                    'metacortex:my:edit_practice',
                    syllabus_id=syllabus.id
                )
        else:
            messages.error(request, _(u'En error occured while saving syllabus.'))

    context = {'form': form, 'syllabus': syllabus}
    template_path = os.path.join(TEMPLATE_ROOT, 'edit.html')
    return render(request, template_path, context)


def syllabus_practice_show_2011(request, syllabus):
    context = {'syllabus': syllabus}
    template_path = os.path.join(TEMPLATE_ROOT, 'show.html')
    return render(request, template_path, context)


def syllabus_practice_print_2011(request, syllabus):
    template_path = os.path.join(TEMPLATE_ROOT, 'print.html')
    file_name = utf2ascii('{code} {name}'.format(
        code=syllabus.subject.internal_code,
        name=syllabus.subject.name
    ))
    template_context = {'syllabus': syllabus}
    return render_to_pdf(request, template_path, template_context, file_name)

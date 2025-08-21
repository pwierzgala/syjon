import os

from django.contrib import messages
from django.shortcuts import redirect, render

from apps.metacortex.forms.reform_2019.forms import SyllabusModuleForm
from apps.syjon.lib.functions import utf2ascii
from apps.syjon.lib.pdf import render_to_pdf

TEMPLATE_ROOT = 'metacortex/syllabus_my/reform_2019/module/'


def syllabus_module_edit_2019(request, syllabus):
    form = SyllabusModuleForm(request.POST or None, instance=syllabus)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Sylabus został zapisany.")

            if 'save' in request.POST:
                return redirect('metacortex:my:show')
            else:
                return redirect(
                    'metacortex:my:edit_module',
                    syllabus_id=syllabus.id
                )
        else:
            messages.error(request, "Wystąpił błąd podczas zapisywania sylabusa")

    context = {
        'form': form,
        'syllabus': syllabus
    }
    template_path = os.path.join(TEMPLATE_ROOT, 'edit.html')
    return render(request, template_path, context)


def syllabus_module_show_2019(request, syllabus):
    context = {'syllabus': syllabus}
    template_path = os.path.join(TEMPLATE_ROOT, 'show.html')
    return render(request, template_path, context)


def syllabus_module_print_2019(request, syllabus):
    template_path = os.path.join(TEMPLATE_ROOT, 'print.html')
    file_name = utf2ascii('{code} {name}'.format(
        code=syllabus.module.internal_code,
        name=syllabus.module.name
    ))
    template_context = {'syllabus': syllabus}
    return render_to_pdf(request, template_path, template_context, file_name)

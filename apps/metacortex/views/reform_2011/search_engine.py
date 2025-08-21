import os

from django.shortcuts import render

from apps.metacortex.models import SyllabusModule

TEMPLATE_ROOT = 'metacortex/search_engine/reform_2011/'


def syllabus_show_2011(request, syllabus):
    if isinstance(syllabus, SyllabusModule):
        template_path = os.path.join(TEMPLATE_ROOT, 'syllabus_show_module.html')
    else:
        template_path = os.path.join(TEMPLATE_ROOT, 'syllabus_show_subject.html')
    context = {'syllabus': syllabus}
    return render(request, template_path, context)

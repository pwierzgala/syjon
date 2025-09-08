import os

from django.contrib import messages
from django.shortcuts import render

from apps.metacortex.forms.reform_2019.forms import SyllabusFilterForm
from apps.metacortex.models import SyllabusModule, SyllabusSubject
from apps.metacortex.settings import (
    SYLLABUS_TYPE_MODULE_ID, SYLLABUS_TYPE_PRACTICE_ID)

TEMPLATE_ROOT = 'metacortex/syllabus_my/reform_2019/'


def show_2019(request, teacher, year, semester, syllabus_type):
    if syllabus_type == SYLLABUS_TYPE_PRACTICE_ID:
        messages.error(request, "Sylabus praktyk nie jest wspierany od 2019 roku.")

    if syllabus_type == SYLLABUS_TYPE_MODULE_ID:
        syllabuses = SyllabusModule.objects.list(teacher, year, semester)
        template_path = os.path.join(TEMPLATE_ROOT, "module", "list.html")
    else:
        syllabuses = SyllabusSubject.objects.list(teacher, year, semester)
        template_path = os.path.join(TEMPLATE_ROOT, "subject", "list.html")

    form = SyllabusFilterForm(
        initial={
            'year': year,
            'semester': semester,
            'type': syllabus_type
        }
    )
    context = {
        'syllabuses': syllabuses,
        'form': form
    }

    return render(request, template_path, context)

import os

from django.shortcuts import render

from apps.metacortex.forms.reform_2011.forms import SyllabusFilterForm
from apps.metacortex.models import (SyllabusModule, SyllabusPractice,
                                    SyllabusSubject)
from apps.metacortex.settings import (SYLLABUS_TYPE_MODULE_ID,
                                      SYLLABUS_TYPE_SUBJECT_ID)

TEMPLATE_ROOT = 'metacortex/syllabus_my/reform_2011/'


def show_2011(request, teacher, year, semester, syllabus_type):

    if syllabus_type == SYLLABUS_TYPE_MODULE_ID:
        syllabuses = SyllabusModule.objects.list(teacher, year, semester)
        template_path = os.path.join(TEMPLATE_ROOT, "module", "list.html")
    elif syllabus_type == SYLLABUS_TYPE_SUBJECT_ID:
        syllabuses = SyllabusSubject.objects.list(teacher, year, semester)
        template_path = os.path.join(TEMPLATE_ROOT, "subject", "list.html")
    else:
        syllabuses = SyllabusPractice.objects.list(teacher, year, semester)
        template_path = os.path.join(TEMPLATE_ROOT, "practice", "list.html")

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

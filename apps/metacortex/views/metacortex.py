# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.metacortex.forms.reform_2019.forms import SyllabusToEctsForm
from apps.metacortex.models import (
    ECTS, SyllabusModule, SyllabusSubject, SyllabusToECTS)

TEMPLATE_ROOT = 'metacortex/'


@login_required
def confirm(request, syllabus_from_id, syllabus_to_id):
    if request.method == 'POST':
        if request.POST.get('action', '') == 'yes':
            return redirect(
                'metacortex:my:copy_subject',
                syllabus_to_id=syllabus_to_id,
                syllabus_from_id=syllabus_from_id
            )
        elif request.POST.get('action', '') == 'no':
            return redirect('metacortex:my:subject_copy_list', syllabus_id=syllabus_from_id)
    else:
        syllabus_to = get_object_or_404(SyllabusSubject, id=syllabus_to_id)
        syllabus_from = get_object_or_404(SyllabusSubject, id=syllabus_from_id)
        kwargs = {'syllabus_from': syllabus_from, 'syllabus_to': syllabus_to}
        return render(request, 'metacortex/syllabus_my/confirm_copy.html', kwargs)


@login_required
def confirm_sm(request, syllabus_from_id, syllabus_to_id):
    if request.method == 'POST':
        if request.POST.get('action', '') == 'yes':
            return redirect(
                'metacortex:my:copy_module',
                syllabus_to_id=syllabus_to_id,
                syllabus_from_id=syllabus_from_id
            )
        else:
            return redirect('metacortex:my:module_copy_list', syllabus_id=syllabus_from_id)
    else:
        syllabus_to = get_object_or_404(SyllabusModule, id=syllabus_to_id)
        syllabus_from = get_object_or_404(SyllabusModule, id=syllabus_from_id)
        kwargs = {'syllabus_from': syllabus_from, 'syllabus_to': syllabus_to}
        return render(request, 'metacortex/syllabus_my/confirm_copy.html', kwargs)


def show_help(request):
    kwargs = {}
    return render(request, TEMPLATE_ROOT+'show_help.html', kwargs)


# --------------------------------------------------------------------------------------
# --- ECTS 2011
# --------------------------------------------------------------------------------------

def save_ects(syllabus, request):
    """
    @param syllabus: Obiekt edytowanego sylabusa.
    """
    if syllabus.get_ects():
        # Zapisanie nowego pola z ekwiwalentem punktów ECTS
        custom_ects_name = request.POST['custom_ects_name'].strip()
        if len(custom_ects_name) != 0:  # Użytkownik zdefiniował własny ekwiwalnet punktów ECTS
            custom_ects_value = request.POST['custom_ects_value']
            custom_ects_value = custom_ects_value.replace(',', '.')
            try:
                custom_ects_value = float(custom_ects_value)
            except ValueError:
                custom_ects_value = 0
            ects = ECTS.objects.create(name=custom_ects_name, order=0)
            SyllabusToECTS.objects.create(syllabus=syllabus, ects=ects, hours=custom_ects_value)

        # Zapisanie istniejących pól z ekwiwalentem punktów ECTS
        ects_ids = request.POST.getlist('ects')
        for ects_id in ects_ids:
            hours = request.POST['ects_'+str(ects_id)]  # Pobranie wkwiwalentu godzinowego z pola tekstowego
            hours = hours.replace(',', '.')  # Zamiana separatora ',' na '.'
            try:
                hours = float(hours)
            except ValueError:
                hours = 0

            if hours is None or hours == '':
                hours = 0

            ects = ECTS.objects.get(id=ects_id)
            syllabus_to_ects = SyllabusToECTS.objects.get(syllabus=syllabus, ects=ects)
            syllabus_to_ects.hours = hours
            syllabus_to_ects.save()

# -*- coding: utf-8 -*-
import os
from collections import OrderedDict

from django import template

from apps.merovingian.models import SubjectType

register = template.Library()

TEMPLATE_ROOT = 'metacortex/templatetags/reform_2011/'


@register.inclusion_tag(os.path.join(TEMPLATE_ROOT, "module_details.html"))
def module_details_table(module):
    details = OrderedDict()
    semesters = range(1, module.get_course().semesters + 1)
    has_module_properties = True if module.moduleproperties_set.all().count() else False
    for semester in semesters:
        details[semester] = []

        if has_module_properties:
            subjects = module.moduleproperties_set.filter(semester=semester)
        else:
            subjects = module.subjects.filter(semester=semester)

        if subjects.count():
            subject_type_ids = subjects.order_by('type').values_list('type', flat=True).distinct()
            for subject_type_id in subject_type_ids:
                subject_type = SubjectType.objects.get(id=subject_type_id)

                subject_group = {'type': subject_type, 'hours': 0, 'ects': 0}
                subjects_by_type = subjects.filter(type=subject_type)
                for subject_by_type in subjects_by_type:
                    subject_group['hours'] += subject_by_type.hours
                    subject_group['ects'] += subject_by_type.ects if subject_by_type.ects else 0

                details[semester].append(subject_group)

        total_hours = 0
        total_ects = 0
        for subject_group in details.values():
            for subject in subject_group:
                total_hours += subject['hours']
                total_ects += subject['ects']

    return {
        'details': details,
        'total_hours': total_hours,
        'total_ects': total_ects
    }


@register.inclusion_tag(os.path.join(TEMPLATE_ROOT, "ects.html"))
def ects(syllabus):
    """
    Wyświetla sekecję pozwalającą na definiowanie punktów ECTS dla sylabusa.
    Sekcja ECTS nie powinna być wyświetlana dla sylabusa, który nie ma przyporządkowanej liczby punktów ECTS.
    """

    # Jezeli kiedys ta wartość się zmieni (30) wtedy trzeba będzie ją przenieść do
    # bazy danych i definiować ją oddzielnie dla każdego semestru.
    all_hours = syllabus.get_ects()*30

    remain_hours = all_hours
    for equivalent in syllabus.syllabus_to_ects.all():
        if equivalent.hours:
            remain_hours -= equivalent.hours

    show_remain_hours_warning = False
    if remain_hours < 0:
        show_remain_hours_warning = True

    return {
        'syllabus': syllabus,
        'remain_hours': remain_hours,
        'show_remain_hours_warning': show_remain_hours_warning
    }

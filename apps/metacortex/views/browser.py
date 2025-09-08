import os
from collections import OrderedDict

from django.shortcuts import get_object_or_404, render

from apps.merovingian.models import Course, Subject, SubjectToTeacher
from apps.metacortex.models import (
    SyllabusModule, SyllabusPractice, SyllabusSubject)
from apps.metacortex.settings import SUBJECT_TYPE_PRACTICE_ID

TEMPLATE_ROOT = 'metacortex/browser/'


def select_semester(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if course.semesters:
        semesters = (s+1 for s in range(course.semesters))
    else:
        semesters = (s+1 for s in range(course.years))
        
    kwargs = {
        'course': course,
        'semesters': semesters
    }

    if course.reform_2019():
        template_path = os.path.join(TEMPLATE_ROOT, 'reform_2019', 'select_semester.html')
    else:
        template_path = os.path.join(TEMPLATE_ROOT, 'reform_2011', 'select_semester.html')

    return render(request, template_path, kwargs)


def supervise(request, course_id, semester):
    course = get_object_or_404(Course, pk=course_id)
    
    # Pobranie wszystkich przedmiotów dla zadanego kierunku i semestru
    subjects = Subject.objects.filter(
        semester=semester,
        module__sgroup__course=course,
        module__sgroup__course__is_active=True,
        module__sgroup__is_active=True,
        module__is_active=True
    )
    
    # Pobranie wszystkich nauczycieli i ich sylabusów powiązanych z przedmiotem
    subjects_dict = {}
    for subject in subjects:
        subjects_dict[subject] = {}
        subject_to_teachers = SubjectToTeacher.objects.filter(subject=subject)
        for subject_to_teacher in subject_to_teachers:
            teacher = subject_to_teacher.teacher
            if subject.type.id == SUBJECT_TYPE_PRACTICE_ID:  # Praktyki
                syllabus = get_or_none(SyllabusPractice, teacher=teacher, subject=subject, is_active=True, is_published=True)
            else:  # Przedmiot
                syllabus = get_or_none(SyllabusSubject, teacher=teacher, subject=subject, is_active=True, is_published=True)
            
            subjects_dict[subject][teacher] = syllabus
    
    # Pogrupowanie przedmiotów modułami
    modules_dict = {}
    for subject, s_value in subjects_dict.items():
        module = subject.module
        if module not in modules_dict:
            modules_dict[module] = {}
            modules_dict[module]['syllabus'] = get_or_none(SyllabusModule, module=module, is_active=True)
            modules_dict[module]['subjects'] = {}
        modules_dict[module]['subjects'][subject] = s_value
    
    # Pogrupowanie modułów specjalnościami
    sgroups_dict = {}
    for module, m_value in modules_dict.items():
        sgroup = module.sgroup
        if sgroup not in sgroups_dict:
            sgroups_dict[sgroup] = {}
        sgroups_dict[sgroup][module] = m_value
        
    kwargs = {
        'SUBJECT_TYPE_PRACTICE_ID': SUBJECT_TYPE_PRACTICE_ID,
        'sgroups': sgroups_dict,
        'course': course,
        'semester': semester
    }

    if course.reform_2019():
        template_path = os.path.join(TEMPLATE_ROOT, 'reform_2019', 'supervise.html')
    else:
        template_path = os.path.join(TEMPLATE_ROOT, 'reform_2011', 'supervise.html')

    return render(request, template_path, kwargs)


def browse(request, course_id, semester):
    course = get_object_or_404(Course, pk=course_id)

    # Pobranie wszystkich przedmiotów dla zadanego kierunku i semestru
    subjects = Subject.objects.filter(
        semester=semester,
        module__sgroup__course=course,
        module__sgroup__course__is_active=True,
        module__sgroup__is_active=True,
        module__is_active=True
    )

    # Pobranie wszystkich nauczycieli i ich sylabusów powiązanych z przedmiotem
    subjects_dict = {}
    for subject in subjects:
        subjects_dict[subject] = {}
        if subject.type.id == SUBJECT_TYPE_PRACTICE_ID:  # Praktyki
            syllabuses = SyllabusPractice.objects.filter(subject=subject, is_active=True, is_published=True)
            for syllabus in syllabuses:
                subjects_dict[subject][syllabus.teacher] = syllabus
        else:
            syllabuses = SyllabusSubject.objects.filter(subject=subject, is_active=True, is_published=True)
            for syllabus in syllabuses:
                subjects_dict[subject][syllabus.teacher] = syllabus

    # Pogrupowanie przedmiotów modułami
    modules_dict = {}
    for subject, s_value in subjects_dict.items():
        module = subject.module
        if module not in modules_dict:
            modules_dict[module] = {}
            syllabus = get_or_none(SyllabusModule, module=module, is_active=True)
            modules_dict[module]['syllabus'] = syllabus
            modules_dict[module]['subjects'] = {}
        modules_dict[module]['subjects'][subject] = s_value

    modules_dict = OrderedDict(sorted(modules_dict.items(), key=lambda x: x[0].name))

    # Pogrupowanie modułów specjalnościami
    sgroups_dict = {}
    for module, m_value in modules_dict.items():
        sgroup = module.sgroup
        if sgroup not in sgroups_dict:
            sgroups_dict[sgroup] = OrderedDict()
        sgroups_dict[sgroup][module] = m_value

    kwargs = {
        'SUBJECT_TYPE_PRACTICE_ID': SUBJECT_TYPE_PRACTICE_ID,
        'sgroups': sgroups_dict,
        'course': course,
        'semester': semester
    }

    if course.reform_2019():
        template_path = os.path.join(TEMPLATE_ROOT, 'reform_2019', 'browse.html')
    else:
        template_path = os.path.join(TEMPLATE_ROOT, 'reform_2011', 'browse.html')

    return render(request, template_path, kwargs)


def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None

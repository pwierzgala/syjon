import os

from django.db.models import Q, Sum
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from apps.merovingian.functions import *
from apps.merovingian.models import *

TEMPLATE_ROOT = "merovingian/study/reform_2019"


def studies_plan_2019(request, sg_b):
    def f(modules, sem):
        # Get type names configuration
        lecture = lecture_name()
        exercise = exercise_name()
        laboratory = laboratory_name()
        conversation = conversation_name()
        seminar = seminar_name()
        facultative = elective_facultative_module_name()

        # Prepare empty results
        result = []
        lecture_sum_all = [0] * (sem + 1)
        exercise_sum_all = [0] * (sem + 1)
        laboratory_sum_all = [0] * (sem + 1)
        conversation_sum_all = [0] * (sem + 1)
        seminar_sum_all = [0] * (sem + 1)
        ects_sum_all = [0] * (sem + 1)
        
        # Load additional data required for calculations
        
        all_subjects = Subject.objects.filter(module__in=modules)
        all_module_properties = ModuleProperties.objects.filter(module__in=modules)
        
        def _semester_subjects(all_subjects, module, semester):
            result = []
            for s in all_subjects: 
                if s.module == module and s.semester == semester:
                    result.append(s)
            return result
        
        def _get_assessment(subjects, examination_name):
            for s in subjects:
                if s.assessment.name == examination_name:
                    return 'E'
            return 'Z' if len(subjects) > 0 else ''
        
        def _semester_module_properties(all_properties, module, semester):
            result = []
            for mp in all_properties: 
                if mp.module == module and mp.semester == semester:
                    result.append(mp)
            return result

        def _sum_hours(subjects, type_name):
            hours = 0
            for info in subjects:
                if info.type and info.type.name == type_name:
                    hours += info.hours if info.hours else 0
                    if info.hours is None:
                        print(type(info))
            return hours
        
        def _sum_ects(subjects):
            ects = 0
            for info in subjects:
                if info.ects:
                    ects += info.ects
            return ects
        
        # ---
        for m in modules:
            hours = []
            for i in range(1, sem + 1):
                subjects = _semester_subjects(all_subjects, m, i)
                properties = _semester_module_properties(all_module_properties, m, i)
                assessment = _get_assessment(subjects, examination_name())
                      
                if len(subjects) > 0 or len(properties) > 0:
                    if m.type is not None and m.type.name == facultative and len(properties) > 0:
                        t = properties
                    else:
                        t = subjects
                        
                    lecture_sum = _sum_hours(t, lecture)
                    exercise_sum = _sum_hours(t, exercise)
                    laboratory_sum = _sum_hours(t, laboratory)
                    conversation_sum = _sum_hours(t, conversation)
                    seminar_sum = _sum_hours(t, seminar)
                    ects_sum = _sum_ects(t)

                    lecture_sum_all[i] += lecture_sum
                    exercise_sum_all[i] += exercise_sum
                    laboratory_sum_all[i] += laboratory_sum
                    conversation_sum_all[i] += conversation_sum
                    seminar_sum_all[i] += seminar_sum
                    ects_sum_all[i] += ects_sum

                    hours.append([
                        lecture_sum,
                        exercise_sum,
                        laboratory_sum,
                        conversation_sum,
                        seminar_sum,
                        ects_sum,
                        assessment
                    ])
                else:
                    hours.append([0, 0, 0, 0, 0, 0, ''])

            if m.type is not None and m.type.name == facultative:
                t = ModuleProperties.objects.filter(module__exact=m)
            else:
                t = Subject.objects.filter(module__exact=m)
            result.append({
                'module': m,
                'lecture_sum': t.filter(type__name=lecture).aggregate(Sum('hours')).get('hours__sum', 0),
                'exercise_sum': t.filter(type__name=exercise).aggregate(Sum('hours')).get('hours__sum', 0),
                'laboratory_sum': t.filter(type__name=laboratory).aggregate(Sum('hours')).get('hours__sum', 0),
                'conversation_sum': t.filter(type__name=conversation).aggregate(Sum('hours')).get('hours__sum', 0),
                'seminar_sum': t.filter(type__name=seminar).aggregate(Sum('hours')).get('hours__sum', 0),
                'hours': hours
            })
            
        tmp_result = result
        result = []
        for i in range(1, sem + 1):
            for r in tmp_result:
                if r in result:
                    continue
                if sum(r['hours'][i-1][0:6]) > 0:
                    result.append(r)

        hours = []
        for i in range(1, sem + 1):
            hours.append([
                lecture_sum_all[i],
                exercise_sum_all[i],
                laboratory_sum_all[i],
                conversation_sum_all[i],
                seminar_sum_all[i],
                ects_sum_all[i],
                ''
            ])
        result.append({
            'module': {'id': None, 'name': 'Suma', 'ects': modules.aggregate(Sum('ects')).get('ects__sum', 0)},
            'lecture_sum': sum(lecture_sum_all),
            'exercise_sum': sum(exercise_sum_all),
            'laboratory_sum': sum(laboratory_sum_all),
            'conversation_sum': sum(conversation_sum_all),
            'seminar_sum': sum(seminar_sum_all),
            'hours': hours
        })
        return result

    obligatory = obligatory_module_name()
    speciality = speciality_module_name()
    specialisation = specialisation_module_name()
    elective = elective_module_name()
    facultative = elective_facultative_module_name()
    
    sem = sg_b.course.years if sg_b.course.years else sg_b.course.semesters 
    
    # if specialty is not whole course
    if sg_b.name != default_sgroup_name():
        # Obligatory modules from whole course and current specialty
        modules_a = f(Module.objects.filter(
            Q(sgroup__exact=sg_b.sgroup, type__name__exact=obligatory) |
            Q(sgroup__exact=sg_b, type__name__exact=obligatory)
        ), sem)

        # Specialty modules from current specialty
        modules_b = f(Module.objects.filter(
            Q(sgroup__exact=sg_b, type__name__exact=speciality) |
            Q(sgroup__exact=sg_b, type__name__exact=specialisation)
        ), sem)

        # Elective modules from whole course and current specialty
        modules_c = f(Module.objects.filter(
            Q(sgroup__exact=sg_b.sgroup, type__name__exact=elective) |
            Q(sgroup__exact=sg_b.sgroup, type__name__exact=facultative) |
            Q(sgroup__exact=sg_b, type__name__exact=elective) |
            Q(sgroup__exact=sg_b, type__name__exact=facultative)
        ), sem)
        modules_name = [_(u'Obligatory modules'), _(u'Specialty/Specialization modules'), _(u'Elective modules')]
        modules = [modules_a, modules_b, modules_c]
    else:
        # Obligatory modules from whole course
        modules_a = f(Module.objects.filter(sgroup__exact=sg_b).exclude(
            Q(type__name__exact=elective) |
            Q(type__name__exact=facultative)
        ), sem)

        # Elective modules from whole course
        modules_b = f(Module.objects.filter(sgroup__exact=sg_b).filter(
            Q(type__name__exact=elective) |
            Q(type__name__exact=facultative)
        ), sem)
        modules_name = [_(u'Obligatory modules'), _(u'Elective modules')]
        modules = [modules_a, modules_b]
    
    plan = {
        'sgroup': sg_b,
        'sem': range(sem),
        'sem_col': range(7),
        'all_col': sem * 7,
        'modules_name': modules_name,
        'modules': modules
    }

    # https://docs.djangoproject.com/en/1.8/ref/models/conditional-expressions/
    # Wziąć pod uwagę ModuleProperties
    # Wziąć pod uwagę kierunki rozliczane rocznie

    kwargs = {
        'plan': plan,
        'course': sg_b.course,
        'sgroup': sg_b,
        'default_sgroup_name': default_sgroup_name(),
        'url': request.build_absolute_uri()
    }

    template_path = os.path.join(TEMPLATE_ROOT, "plan.html")
    return render(request, template_path, kwargs)

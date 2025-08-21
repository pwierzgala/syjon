# -*- coding: utf-8 -*-

from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.utils.translation import ugettext as _


def user_courses(user):
    """
    Return list of courses that user can modify.
    Superuser can modify all courses.
    Course admin can modify only those courses that are attached to him
    and are in actual or future didactic offer.
    """
    from apps.merovingian.models import Course, MerovingianAdmin
    if user.is_superuser:
        return Course.objects.all()
    elif user.is_authenticated():
        try:
            admin = MerovingianAdmin.objects.get(user_profile__user=user)
            if admin.temporary_privileged_access:
                return admin.courses.active()
            else:
                return admin.courses.didactic_offer_and_future()
        except MerovingianAdmin.DoesNotExist:
            return []
    else:
        return Course.objects.active()

def user_subjects(user):
    """
    Return list of subjects that user can modify.
    Superuser can modify all subjects.
    Major admin can modify only those subjects 
    that are in majors attached to him
    and are in actual or future didactic offer.
    """
    from apps.merovingian.models import Module, Subject
    if user.is_superuser:
        return Subject.objects.all()
    elif user.is_authenticated:
        return Subject.objects.didactic_offer().filter(module__in=Module.objects.active().filter(
            sgroup__course__in=user_courses(user),
            sgroup__course__is_active=True,
            sgroup__is_active=True))
    else:
        return []

def item_per_page():
    from apps.merovingian.models import MerovingianSettings
    try:
        return int(MerovingianSettings.objects.get(key = 'item_per_page').value)
    except (MerovingianSettings.DoesNotExist, ValueError):
        return 25

def make_page(request, objects, objects_id = 'merv'):
    """
    """
    paginator = Paginator(objects, item_per_page())
    try:
        page = request.GET.get('page', None)
        objects_cnt = paginator.count 
        if objects_id is not None:
            if abs(objects_cnt - request.session.get(objects_id + '_objects', objects_cnt)) > 1:
                objects_page = paginator.page(1)
            elif page is not None:
                objects_page = paginator.page(int(page))
            else:
                objects_page = paginator.page(int(request.session.get(objects_id + '_page', '1')))
        else: 
            objects_page = paginator.page(int(page))
    except (TypeError, ValueError, EmptyPage, InvalidPage):
        objects_page = paginator.page(1)
    finally:
        if objects_id is not None:
            request.session[objects_id + '_page'] = objects_page.number
            request.session[objects_id + '_objects'] = objects_cnt
        return objects_page

def ects_per_semester():
    from apps.merovingian.models import MerovingianSettings
    try:
        return float(MerovingianSettings.objects.get(key = 'ects_per_semester').value)
    except (MerovingianSettings.DoesNotExist, ValueError):
        return 30.0

def default_sgroup_settings():
    from apps.merovingian.models import MerovingianSettings
    try:
        return MerovingianSettings.objects.get(key = 'default_sgroup_name')
    except MerovingianSettings.DoesNotExist:
        raise RuntimeError('Undefined merv setting "%s"' % 'default_sgroup_name')

def default_sgroup_name():
    return default_sgroup_settings().value

def lecture_name():
    from apps.merovingian.models import MerovingianSettings
    try:
        return MerovingianSettings.objects.get(key = 'lecture_name').value
    except MerovingianSettings.DoesNotExist:
        raise RuntimeError('Undefined merv setting "%s"' % 'lecture_name')

def exercise_name():
    from apps.merovingian.models import MerovingianSettings
    try:
        return MerovingianSettings.objects.get(key = 'exercise_name').value
    except MerovingianSettings.DoesNotExist:
        raise RuntimeError('Undefined merv setting "%s"' % 'exercise_name')

def laboratory_name():
    from apps.merovingian.models import MerovingianSettings
    try:
        return MerovingianSettings.objects.get(key = 'laboratory_name').value
    except MerovingianSettings.DoesNotExist:
        raise RuntimeError('Undefined merv setting "%s"' % 'laboratory_name')

def conversation_name():
    from apps.merovingian.models import MerovingianSettings
    try:
        return MerovingianSettings.objects.get(key = 'conversation_name').value
    except MerovingianSettings.DoesNotExist:
        raise RuntimeError('Undefined merv setting "%s"' % 'conversation_name')

def seminar_name():
    from apps.merovingian.models import MerovingianSettings
    try:
        return MerovingianSettings.objects.get(key = 'seminar_name').value
    except MerovingianSettings.DoesNotExist:
        raise RuntimeError('Undefined merv setting "%s"' % 'seminar_name')

def examination_name():
    from apps.merovingian.models import MerovingianSettings
    try:
        return MerovingianSettings.objects.get(key = 'examination_name').value
    except MerovingianSettings.DoesNotExist:
        raise RuntimeError('Undefined merv setting "%s"' % 'examination_name')

def pass_name():
    from apps.merovingian.models import MerovingianSettings
    try:
        return MerovingianSettings.objects.get(key = 'pass_name').value
    except MerovingianSettings.DoesNotExist:
        raise RuntimeError('Undefined merv setting "%s"' % 'pass_name')

def assessment_name():
    from apps.merovingian.models import MerovingianSettings
    try:
        return MerovingianSettings.objects.get(key = 'assessment_name').value
    except MerovingianSettings.DoesNotExist:
        raise RuntimeError('Undefined merv setting "%s"' % 'assessment_name')

def obligatory_module_name():
    from apps.merovingian.models import MerovingianSettings
    try:
        return MerovingianSettings.objects.get(key = 'obligatory_module_name').value
    except MerovingianSettings.DoesNotExist:
        raise RuntimeError('Undefined merv setting "%s"' % 'obligatory_module_name')

def elective_module_name():
    from apps.merovingian.models import MerovingianSettings
    try:
        return MerovingianSettings.objects.get(key = 'elective_module_name').value
    except MerovingianSettings.DoesNotExist:
        raise RuntimeError('Undefined merv setting "%s"' % 'elective_module_name')

def elective_facultative_module_name():
    from apps.merovingian.models import MerovingianSettings
    try:
        return MerovingianSettings.objects.get(key = 'elective_facultative_module_name').value
    except MerovingianSettings.DoesNotExist:
        raise RuntimeError('Undefined merv setting "%s"' % 'elective_facultative_module_name')

def academic_module_name():
    from apps.merovingian.models import MerovingianSettings
    try:
        return MerovingianSettings.objects.get(key = 'academic_module_name').value
    except MerovingianSettings.DoesNotExist:
        raise RuntimeError('Undefined merv setting "%s"' % 'academic_module_name')

def speciality_module_name():
    from apps.merovingian.models import MerovingianSettings
    try:
        return MerovingianSettings.objects.get(key = 'speciality_module_name').value
    except MerovingianSettings.DoesNotExist:
        raise RuntimeError('Undefined merv setting "%s"' % 'speciality_module_name')

def specialisation_module_name():
    from apps.merovingian.models import MerovingianSettings
    try:
        return MerovingianSettings.objects.get(key = 'specialisation_module_name').value
    except MerovingianSettings.DoesNotExist:
        raise RuntimeError('Undefined merv setting "%s"' % 'specialisation_module_name')

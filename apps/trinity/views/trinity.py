# -*- coding: utf-8 -*-

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _

from apps.merovingian.models import Course
from apps.trinity.models import AreaLearningOutcome, TrinityProfile


def is_learning_outcomes_administrator(user, course):
    """
    Returns True if user can manage learning outcomes connected with specified speciality.
    @param user: User object
    @param course: Course object 
    """
    if user.is_superuser:
        return True
    
    is_administrator = False
    
    try:
        trinity_profile = user.userprofile.trinityprofile  # Gets user's learning outcomes administrator profile
        if course in trinity_profile.courses.all():  # Checkes if user has rights to speciality passed as a parameter
            is_administrator = True
    except TrinityProfile.DoesNotExist:
        is_administrator = False
    except AttributeError:
        is_administrator = False
    
    return is_administrator


def trinity_administrator_required(func):

    def _trinity_administrator_required(request, course_id, *args, **kwargs):
        course = get_object_or_404(Course, pk=course_id)
        if is_learning_outcomes_administrator(request.user, course):
            return func(request, course_id, *args, **kwargs)
        else:
            messages.error(request, _("You do not have permission to execute selected operation"))
            return redirect('merovingian:course:details', course_id=course.id)

    return _trinity_administrator_required


def get_alos_for_course(course, education_category):
    """
    Pobiera obszarowe efekty kształcenia dla przekazanej w parametrach konfiguracji.
    Dla studiów magisterskich i inżynieryjnych pobierane są obszarowe efekty ksztalcenia z poziomu I i II.
    @param course: Kierunek
    @param education_category: Kategoria kształcenia np. wiedza, umiejętności.
    """

    alos = AreaLearningOutcome.objects.filter(
        education_area__in=course.education_areas.all(),
        education_category=education_category,
        education_profile=course.profile
    )

    if course.is_level_ba() or course.is_level_msc():
        alos = alos.filter(education_level=course.level)

    return alos

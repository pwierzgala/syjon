from django.shortcuts import render

from apps.merovingian.functions import default_sgroup_name
from apps.merovingian.models import Course, MerovingianAdmin
from apps.trinity.views.trinity import is_learning_outcomes_administrator


def show_2019(request, course):
    show_archived = True if request.GET.get('archived', False) else False

    # Limit courses visibility only for Wydział Artystyczny.
    art_department_id = 25
    if course.department.id == art_department_id:
        course_manager = Course.objects.active() if show_archived else Course.objects.didactic_offer_and_future()
    else:
        course_manager = Course.objects.active()
    all_courses = course_manager.filter(name=course.name).order_by('-start_date', 'level')
                   
    # Other years and levels     
    courses_years = []
    for m in all_courses:
        if m.start_date:
            year = m.start_date.year
            if year not in [y['class_year'] for y in courses_years]:
                courses_years.append({
                    'class_year': year,
                    'study_year': m.get_current_year()
                })
            else:
                if m.get_current_year() is not None:
                    list(filter(lambda z: z['class_year'] == year, courses_years))[0]['study_year'] = m.get_current_year()
                
    # Merovingian admin check
    user_merv_admin = None
    if request.user.is_authenticated:
        try:
            user_merv_admin = MerovingianAdmin.objects.get(user_profile=request.user.userprofile)
        except MerovingianAdmin.DoesNotExist:
            user_merv_admin = None
    
    # Learning outcomes administrator check
    is_learning_outcomes_admin = is_learning_outcomes_administrator(request.user, course)

    # Template variables
    kwargs = {
        'course': course,
        'default_sgroup_name': default_sgroup_name(),
        'courses_years': courses_years,
        'all_courses': all_courses,
        'user_merv_admin': user_merv_admin,
        'is_course_in_active_offer': course.is_in_active_offer(),
        'is_learning_outcomes_admin': is_learning_outcomes_admin,
        'show_archived': show_archived,
    }
    return render(request, 'merovingian/courses/reform_2019/show.html', kwargs)

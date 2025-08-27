from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models.aggregates import Max
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from apps.merovingian.forms.forms import (CourseForm, SearchFilterForm,
                                          SGroupInlineFormset)
from apps.merovingian.functions import make_page
from apps.merovingian.models import Course, MerovingianAdmin, SGroup
from apps.merovingian.views.reform_2011.course import show_2011
from apps.merovingian.views.reform_2019.course import show_2019
from apps.trainman.models import Department, UserProfile

# --- Courses Views ---


def index(request, department_id=None):
    
    column_name = 'name_' + translation.get_language()
    courses_names = Course.objects.active().values(column_name).distinct(

    ).annotate(id=Max('id')).order_by(column_name)

    course_name = request.session.get('merv_courses_names_search', '')

    if request.method == 'POST':
        search_form = SearchFilterForm(request.POST)
        if search_form.is_valid():
            course_name = request.session['merv_courses_names_search'] = search_form.cleaned_data['name']
            department = search_form.cleaned_data['department']
            if department is None:
                return redirect('merovingian:course:list')
            else:
                return redirect('merovingian:course:list', department_id=department.id)
    else:
        search_form = SearchFilterForm(initial={'name': course_name, 'faculty': department_id})

    if course_name:
        filters = {column_name+'__icontains': course_name}
        courses_names = courses_names.filter(**filters)

    if department_id is not None:
        department = get_object_or_404(Department, id=department_id)
        departments_ids = department.children_id()
        courses_names = courses_names.filter(department__id__in=departments_ids)

    courses_names_page = make_page(request, courses_names, 'merv_courses_names')
    courses_names = [{'id': m['id'], 'name': m[column_name]} for m in courses_names_page.object_list]

    kwargs = {'courses_names_page': courses_names_page, 'courses_names': courses_names, 'search_form': search_form}
    return render(request, 'merovingian/courses/index.html', kwargs)


@login_required
@permission_required('merovingian.add_course')
def add(request):
    course = None
    course_form = CourseForm()
    sgroup_formset = SGroupInlineFormset()

    if request.method == 'POST':
        course_form = CourseForm(request.POST)
        if course_form.is_valid():
            course = course_form.save()
            sgroup_formset = SGroupInlineFormset(request.POST, request.FILES, instance=course)

            if not request.user.is_superuser:
                try:
                    MerovingianAdmin.objects.get_or_create(user_profile=request.user.userprofile)
                except UserProfile.DoesNotExist:
                    user_profile = UserProfile(user=request.user)
                    user_profile.save()
                    merovingian_admin = MerovingianAdmin.objects.create(user_profile=user_profile)
                    merovingian_admin.courses.add(course)

            messages.success(request, _(u'Course %s has been saved succesfully.') % course)

            if sgroup_formset.is_valid():
                sgroup_formset.save()

                if 'save' in request.POST:
                    return redirect('merovingian:course:details', course_id=course.id)
                else:
                    return redirect('merovingian:course:edit', course_id=course.id)
            else:
                messages.error(request, _(u'Correct errors listed below.'))
        else:
            messages.error(request, _(u'Correct errors listed below.'))

    kwargs = {
        'course': course,
        'course_form': course_form,
        'sgroup_formset': sgroup_formset
    }
    return render(request, 'merovingian/courses/course_form.html', kwargs)


def name(request, course_id):
    try:
        course = Course.objects.active().get(id=course_id)
    except Course.DoesNotExist:
        messages.error(request, _(u'Selected course does not exist. If you see this message again, contact the Administrator.'))
        return redirect('merovingian:course:list')

    all_courses = Course.objects.active()\
                        .filter(name=course.name)\
                        .order_by('-start_date', 'level')
                        
    if len(all_courses) == 0:
        newest_course = course
    else:
        newest_course = all_courses[0]
    return redirect('merovingian:course:details', newest_course.id)
    

def show(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        messages.error(request, _(u'Selected course does not exist. If you '
                                  u'see this message again, contact the Administrator.'))
        return redirect('merovingian:course:list')

    if course.reform_2019():
        return show_2019(request, course)
    else:
        return show_2011(request, course)


@login_required
@permission_required('merovingian.change_course')
def edit(request, course_id, sgroup_id=None):
    course = get_object_or_404(Course, id=course_id)

    # Merovingian admin check
    user_merv_admin = None
    if request.user.is_authenticated:
        try:
            user_merv_admin = MerovingianAdmin.objects.get(user_profile=request.user.userprofile)
        except MerovingianAdmin.DoesNotExist:
            user_merv_admin = None

    if not request.user.is_superuser:
        if not user_merv_admin or course not in user_merv_admin.courses.all():
            return HttpResponseNotFound()

    # Check if course is active and forbid access
    if course.is_in_active_offer() and not request.user.is_superuser and not user_merv_admin.temporary_privileged_access:
        messages.error(request, _(u'You cannot edit course that is in active teaching offer.'))
        return redirect('merovingian:course:details', course_id=course.id)

    course_form = CourseForm(request.POST or None, instance=course)
    sgroup_formset = SGroupInlineFormset(request.POST or None, request.FILES or None, instance=course)

    if request.method == 'POST':
        if course_form.is_valid() and sgroup_formset.is_valid():
            course_form.save()
            sgroup_formset.save()

            messages.success(request, _(u'Course %s has been saved succesfully.') % course)

            if 'save' in request.POST:
                return redirect('merovingian:course:details', course_id=course.id)
            else:
                return redirect('merovingian:course:edit', course_id=course.id)
        else:
            messages.error(request, _(u'Correct errors listed below.'))

    sgroup = get_object_or_404(SGroup, id=sgroup_id, course=course) if sgroup_id else None

    kwargs = {
        'course': course,
        'course_form': course_form,
        'sgroup_formset': sgroup_formset,
        'sgroup': sgroup
    }
    return render(request, 'merovingian/courses/course_form.html', kwargs)

from django.contrib.auth.decorators import login_required, permission_required
from django.db.models.aggregates import Max
from django.shortcuts import render
from django.utils import translation

from apps.merovingian.forms.forms import SearchForm
from apps.merovingian.functions import make_page
from apps.merovingian.models import Course, MerovingianAdmin

# --- Courses Views ---


@login_required
@permission_required('merovingian.change_course')
def index(request):
    
    column_name = 'name_' + translation.get_language()
    courses_names = Course.objects.didactic_offer_and_future()
                        
    if not request.user.is_superuser:
        try:
            admin = MerovingianAdmin.objects.get(user_profile=request.user.userprofile)
            courses = admin.courses.all()
        except MerovingianAdmin.DoesNotExist:
            courses = []
        courses_names = courses_names.filter(id__in=courses)
        
    courses_names = courses_names.values(column_name).distinct()\
        .annotate(id=Max('id')).order_by(column_name)

    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            name = request.session['merv_courses_names_search'] = search_form.cleaned_data['name']
    else:
        name = request.session.get('merv_courses_names_search', '')
        search_form = SearchForm(initial = {'name': name})

    if name:
        filters = {column_name+'__icontains': name}
        courses_names = courses_names.filter(**filters)

    courses_names_page = make_page(request, courses_names, 'merv_courses_names')
    courses_names = [{'id': m['id'], 'name': m[column_name]} for m in courses_names_page.object_list]

    kwargs = {
        'courses_names_page': courses_names_page,
        'courses_names': courses_names,
        'search_form': search_form
    }
    return render(request, 'merovingian/courses/index.html', kwargs)


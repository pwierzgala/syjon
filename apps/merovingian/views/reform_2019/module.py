import os

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _

from apps.merovingian.forms.forms import SearchForm
from apps.merovingian.forms.reform_2019.forms import *
from apps.merovingian.functions import *
from apps.merovingian.models import *
from apps.metacortex.models import SyllabusModule, SyllabusSubject

TEMPLATE_ROOT = "merovingian/modules/reform_2019"


def list_2019(request, sgroup):
    # Merovingian admin check
    user_merv_admin = None
    if request.user.is_authenticated():
        try:
            user_merv_admin = MerovingianAdmin.objects.get(
                user_profile=request.user.userprofile)
        except MerovingianAdmin.DoesNotExist:
            user_merv_admin = None

    # Check if course is active and forbid access
    if sgroup.course.is_in_active_offer() and not (
        request.user.is_superuser or user_merv_admin.temporary_privileged_access
    ):
        messages.info(request, _(
            u'You may only modify the facultative modules, because this course is already running.'))

    # Handle search form
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            name = request.session['sgroup_module_' + str(sgroup.id)] = \
                search_form.cleaned_data['name']
    else:
        name = request.session.get('sgroup_module_' + str(sgroup.id), '')
        search_form = SearchForm(initial={'name': name})

    modules = sgroup.modules
    # Choose only facultative modules as the course is already running
    if sgroup.course.is_in_active_offer() and not \
       (request.user.is_superuser or user_merv_admin.temporary_privileged_access):
        modules = modules.filter(type__name__exact=elective_facultative_module_name())

    modules = modules.filter(
        Q(name__istartswith=name) | Q(type__name__istartswith=name))

    kwargs = {
        'sgroup': sgroup,
        'course': sgroup.course,
        'default_sgroup_name': default_sgroup_name(),
        'modules_page': make_page(request, modules, 'sgroup_' + str(sgroup.id)),
        'search_form': search_form,
        'user_merv_admin': user_merv_admin
    }
    template_path = os.path.join(TEMPLATE_ROOT, "list.html")
    return render(request, template_path, kwargs)


def add_2019(request, sgroup):
    # Merovingian admin check
    user_merv_admin = None
    if request.user.is_authenticated():
        try:
            user_merv_admin = MerovingianAdmin.objects.get(
                user_profile=request.user.userprofile)
        except MerovingianAdmin.DoesNotExist:
            user_merv_admin = None

    # Check if course is active and forbid access
    if sgroup.course.is_in_active_offer() and not (
        request.user.is_superuser or user_merv_admin.temporary_privileged_access):
        messages.error(request, _(
            u'You cannot edit course that is in active teaching offer.'))
        return redirect('merovingian:course:details', course_id=sgroup.course.id)

    module = None
    module_form = ModuleForm()
    subject_formset = SubjectInlineFormset()

    if request.method == 'POST':
        # Bind course and subjects forms wit post data
        module_form = ModuleForm(request.POST)
        if module_form.is_valid():
            module = module_form.save(commit=False)
            module.sgroup = sgroup
            subject_formset = SubjectInlineFormset(request.POST, request.FILES,
                                                   instance=module)
            if subject_formset.is_valid():
                module.save()
                subject_formset.save()
                sgroup.modules.add(module)
                messages.success(request, _(
                    u'Module %s has been added succesfully.') % module)

                if request.POST.get('action') == 'save':
                    return redirect('merovingian:module:list', sgroup_id=sgroup.id)
                elif request.POST.get('action') == 'save_and_edit':
                    return redirect('merovingian:module:edit', module_id=module.id)
            else:
                module = None
                messages.error(request, _(u'Correct errors listed below.'))
        else:
            messages.error(request, _(u'Correct errors listed below.'))

    kwargs = {
        'sgroup': sgroup,
        'course': sgroup.course,
        'default_sgroup_name': default_sgroup_name(),
        'module': module,
        'module_form': module_form,
        'subject_formset': subject_formset
    }
    template_path = os.path.join(TEMPLATE_ROOT, "form.html")
    return render(request, template_path, kwargs)


def edit_2019(request, module):
    def is_module_properties(module):
        """
        Returns True if module is elective
        """
        if module.type is None:
            return False
        else:
            return True if module.type.name == elective_facultative_module_name() \
                else False

    sgroup = module.sgroup

    # Merovingian admin check
    user_merv_admin = None
    if request.user.is_authenticated():
        try:
            user_merv_admin = MerovingianAdmin.objects.get(
                user_profile=request.user.userprofile)
        except MerovingianAdmin.DoesNotExist:
            user_merv_admin = None

    # Check if course is active and forbid access
    if sgroup.course.is_in_active_offer() and (
        module.type and module.type.name != elective_facultative_module_name()
    ) and not (
            request.user.is_superuser or
            user_merv_admin.temporary_privileged_access
    ):
        messages.error(request, _(
            u'You cannot modify modules that belongs to course which is in active '
            u'teaching offer.'))
        return redirect('merovingian:course:details', course_id=sgroup.course.id)

    if request.method == 'POST':
        module_form = ModuleForm(request.POST, instance=module)
        subject_formset = SubjectInlineFormset(
            request.POST, instance=module
        )
        module_properties_formset = ModulePropertiesInlineFormset(
            request.POST, instance=module)

        if module_form.is_valid() and \
            subject_formset.is_valid() and \
            module_properties_formset.is_valid():
            module_form.save()
            subject_formset.save()

            # Save module properties if module's is elective
            if is_module_properties(module):
                # Rebind saved module to properties formset
                module_properties_formset = ModulePropertiesInlineFormset(
                    request.POST, instance=module)
                module_properties_formset.save()
            else:
                # Remove properties if module is no longer elective
                ModuleProperties.objects.filter(module=module).delete()
            messages.success(
                request,
                _(u'Module %s has been saved succesfully.') % module
            )

            if 'save' in request.POST:
                return redirect('merovingian:module:list', sgroup_id=sgroup.id)
            else:
                return redirect('merovingian:module:edit', module_id=module.id)
        else:
            messages.error(request, _(u'Correct errors listed below.'))
    else:
        module_form = ModuleForm(instance=module)
        subject_formset = SubjectInlineFormset(instance=module)
        module_properties_formset = ModulePropertiesInlineFormset(instance=module)

    kwargs = {
        'sgroup': sgroup,
        'course': sgroup.course,
        'default_sgroup_name': default_sgroup_name(),
        'module': module,
        'module_form': module_form,
        'subject_formset': subject_formset,
        'module_properties': is_module_properties(module),
        'module_properties_formset': module_properties_formset
    }
    template_path = os.path.join(TEMPLATE_ROOT, "form.html")
    return render(request, template_path, kwargs)


def syllabuses_2019(request, module):
    sgroup = module.sgroup

    try:
        syllabus_module = SyllabusModule.objects.published().get(module__exact=module)
    except SyllabusModule.DoesNotExist:
        syllabus_module = None
    kwargs = {
        'course': sgroup.course,
        'sgroup': sgroup,
        'default_sgroup_name': default_sgroup_name(),
        'module': module,
        'syllabus_module': syllabus_module,
        'syllabus_subject': [
            {'s': s, 'ss': SyllabusSubject.objects.published().active().filter(subject__exact=s)} for s in module.subjects.all()
        ],
        'plan': {'sgroup': sgroup}
    }
    template_path = os.path.join(TEMPLATE_ROOT, "syllabuses.html")
    return render(request, template_path, kwargs)

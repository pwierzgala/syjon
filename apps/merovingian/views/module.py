from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _

from apps.merovingian.functions import *
from apps.merovingian.models import *
from apps.merovingian.views.reform_2011.module import (add_2011, edit_2011,
                                                       list_2011,
                                                       syllabuses_2011)
from apps.merovingian.views.reform_2019.module import (add_2019, edit_2019,
                                                       list_2019,
                                                       syllabuses_2019)


def syllabuses(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    course = module.sgroup.course

    if course.reform_2019():
        return syllabuses_2019(request, module)
    else:
        return syllabuses_2011(request, module)


@login_required
def list(request, sgroup_id):
    sgroup = get_object_or_404(SGroup, id=sgroup_id)
    course = sgroup.course

    if course.reform_2019():
        return list_2019(request, sgroup)
    else:
        return list_2011(request, sgroup)


@login_required
@permission_required('merovingian.add_module')
def add(request, sgroup_id):
    sgroup = get_object_or_404(SGroup, id=sgroup_id)
    course = sgroup.course

    if course.reform_2019():
        return add_2019(request, sgroup)
    else:
        return add_2011(request, sgroup)


@login_required
@permission_required('merovingian.change_module')
def edit(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    course = module.sgroup.course

    if course.reform_2019():
        return edit_2019(request, module)
    else:
        return edit_2011(request, module)


@login_required
@permission_required('merovingian.delete_module')
def delete(request, module_id):
    try:
        module = Module.objects.get(id__exact=module_id)
        sgroup = module.sgroup
        
        # Merovingian admin check
        user_merv_admin = None
        if request.user.is_authenticated:
            try:
                user_merv_admin = MerovingianAdmin.objects.get(user_profile=request.user.userprofile)
            except MerovingianAdmin.DoesNotExist:
                user_merv_admin = None
        
        if not request.user.is_superuser:
            user_courses(request.user).get(id__exact=sgroup.course_id)
            
        # Check if course is active and forbid access
        if sgroup.course.is_in_active_offer() and not (request.user.is_superuser or user_merv_admin.temporary_privileged_access):
            messages.error(request, _(u'You cannot edit course that is in active teaching offer.'))
            return redirect('merovingian:course:details', course_id=sgroup.course.id)

    except SGroup.DoesNotExist:
        messages.error(request, _(u'Selected specialty does not exist. If you see this message again, contact the Administrator.'))
        return redirect('merovingian:course:list')
    except Module.DoesNotExist:
        messages.error(request, _(u'Selected module does not exist. If you see this message again, contact the Administrator.'))
        return redirect('merovingian:module:list', sgroup_id=sgroup.id)
    else:
        messages.success(request, _(u'Module %s has been deleted successfully.') % module)
        module.delete()
        return redirect('merovingian:module:list', sgroup_id=sgroup.id)

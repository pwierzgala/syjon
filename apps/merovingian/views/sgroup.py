from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext as _

from apps.merovingian.models import SGroup
from apps.merovingian.views.reform_2011.sgroup import studies_plan_2011
from apps.merovingian.views.reform_2019.sgroup import studies_plan_2019


def studies_plan(request, sgroup_id):
    try:
        sg_b = SGroup.objects.active().get(id=sgroup_id)
    except SGroup.DoesNotExist:
        messages.error(request, _(u'Internal error, please contact the Administrator.'))
        return redirect('apps.merovingian.views.study_sgroup_show')

    course = sg_b.course
    if course.reform_2019():
        return studies_plan_2019(request, sg_b)
    else:
        return studies_plan_2011(request, sg_b)

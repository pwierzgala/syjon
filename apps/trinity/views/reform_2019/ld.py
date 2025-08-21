import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext_lazy as _

from apps.merovingian.models import Course
from apps.trinity.forms import LeadingDisciplineInlineFormset
from apps.trinity.views.trinity import trinity_administrator_required

TEMPLATE_ROOT = 'trinity/leading_discipline/'


@login_required
@trinity_administrator_required
def assign(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    formset = LeadingDisciplineInlineFormset(request.POST or None, instance=course)

    if request.method == 'POST':
        if formset.is_valid():
            for form in formset:
                form.save()
            messages.success(request, _(u'Changes have been successfully saved'))
            return redirect('trinity:ld:assign', course_id=course.id)

    context = {
        'course': course,
        'formset': formset
    }
    template_path = os.path.join(TEMPLATE_ROOT, "assign.html")
    return render(request, template_path, context)

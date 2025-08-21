from django import template
from django.shortcuts import get_object_or_404

from apps.trainman.models import Department

register = template.Library()

@register.filter
def show_lock_app(request):
    institute_of_computer_science = get_object_or_404(Department, name__iexact='Instytut Informatyki')
    return request.user.userprofile.is_in_department(institute_of_computer_science)

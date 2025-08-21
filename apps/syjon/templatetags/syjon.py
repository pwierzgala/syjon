from django import template
from django.conf import settings

register = template.Library()

@register.filter
def is_read_only(request):
    return not request.user.is_superuser and settings.IS_READ_ONLY
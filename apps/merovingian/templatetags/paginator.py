# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.inclusion_tag('merovingian/templatetags/paginator.html')
def paginator(page):
    kwargs = {'page': page}
    return kwargs

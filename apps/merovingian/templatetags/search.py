# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.inclusion_tag('merovingian/templatetags/search.html')
def search(search_form, search_url = ''):
    kwargs = {'search_form': search_form,
              'search_url': search_url}
    return kwargs

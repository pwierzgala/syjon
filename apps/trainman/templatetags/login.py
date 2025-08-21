# -*- coding: utf-8 -*-

from django import template

register = template.Library()

from apps.trainman.forms import LoginForm


@register.inclusion_tag('trainman/templatetags/login_panel.html', takes_context=True)
def login_panel(context):
    request = context['request']
    form = LoginForm()
    return {'request': request, 'form': form}
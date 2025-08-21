# -*- coding: utf-8 -*-

from django import template

register = template.Library()


@register.filter(name='get_parameters_string')
def get_parameters_string(request, exclude_parameter):
    """
    :param request: http request
    :param exclude_parameter: get parameter to be excluded from get parameters in request
    :return: string of get parameters
    """
    get = request.GET.copy()
    if exclude_parameter:
        get.pop(exclude_parameter, None)
    return get.urlencode()


@register.inclusion_tag('syjon/templatetags/render_get_parameters.html')
def render_get_parameters(request, *exclude_parameters):
    """
    :param request: http request
    :param exclude_parameter: get parameter to be excluded from get parameters in request
    :return: template with get parameters rendered as hidden inputs
    """
    parameters = request.GET.copy()
    if exclude_parameters:
        for exclude_parameter in exclude_parameters:
            parameters.pop(exclude_parameter, None)
    return {'parameters': parameters}

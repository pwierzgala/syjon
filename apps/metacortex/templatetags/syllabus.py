from django import template

register = template.Library()


# ---------------------------------------------------
# --- SYLLABUS SEARCH RESULT
# ---------------------------------------------------

@register.inclusion_tag('metacortex/templatetags/syllabus_module_search_result.html')
def syllabus_module_search_result(syllabus):
    return {'syllabus': syllabus}


@register.inclusion_tag('metacortex/templatetags/syllabus_subject_search_result.html')
def syllabus_subject_search_result(syllabus):
    return {'syllabus': syllabus}


@register.inclusion_tag('metacortex/templatetags/syllabus_practice_search_result.html')
def syllabus_practice_search_result(syllabus):
    return {'syllabus': syllabus}

from django import forms
from django.forms.utils import ErrorList
from django.utils.translation import gettext_lazy as _

from apps.merovingian.functions import default_sgroup_name
from apps.merovingian.models import Course, SGroup, SGroupType
from apps.merovingian.translation import (
    TranslatedInlineFormset, TranslatedModelForm)
from apps.trainman.models import DEPARTMENT_TYPE_FACULTY, Department

# ----------------------------------------------------------
# --- SEARCH
# ----------------------------------------------------------

class SearchForm(forms.Form):
    name = forms.CharField(label='', required=False)


class SearchFilterForm(forms.Form):
    name = forms.CharField(label='', required=False)
    department = forms.ModelChoiceField(
        widget=forms.Select(),
        queryset=Department.objects.filter(type_id=DEPARTMENT_TYPE_FACULTY),
        required=False,
        empty_label=_(u"All departments")
    )


# ----------------------------------------------------------
# --- COURSE
# ----------------------------------------------------------

class CourseForm(TranslatedModelForm):
    class Meta:
        model = Course
        exclude = ()
        
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget = forms.DateInput()
        
    def clean(self):
        cleaned_data = super(CourseForm, self).clean()
        if cleaned_data['years'] and cleaned_data['semesters']:
            errors = self._errors.setdefault('semesters', ErrorList())
            errors.append(_(u'Course cannot be settled per year and per semester at the same time. Fill in one field, either number of years ot number of semesters.'))
        return cleaned_data


# ----------------------------------------------------------
# --- SGROUP
# ----------------------------------------------------------

class SGroupBaseInlineFormSet(TranslatedInlineFormset):
    def add_fields(self, form, index):
        super(SGroupBaseInlineFormSet, self).add_fields(form, index)
        form.fields['type'] = forms.ModelChoiceField(queryset=SGroupType.objects.exclude(name=default_sgroup_name()))

    def get_queryset(self):
        return super(SGroupBaseInlineFormSet, self).get_queryset().exclude(name=default_sgroup_name())


SGroupInlineFormset = forms.models.inlineformset_factory(
    Course,
    SGroup,
    exclude=('modules', ),
    formset=SGroupBaseInlineFormSet
)

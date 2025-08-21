# -*- coding: utf-8 -*-

from django import forms
from django.utils.safestring import mark_safe

from apps.merovingian.models import Module, Subject, SubjectToTeacher
from apps.trainman.models import Teacher


class SearchForm(forms.Form):
    name = forms.CharField(label='', required=False)


class LabelHiddenInput(forms.widgets.HiddenInput):
    def render(self, name, value, attrs=None):
        widget = super(LabelHiddenInput, self).render(name, value, attrs)
        label = str(Teacher.objects.get(id = int(value))) if value else u''
        return mark_safe(widget + u'<strong id="id_%s-label">' % (name) + label + u'</strong>')


class SubjectToTeacherBaseFormSet(forms.models.BaseInlineFormSet):
    def add_fields(self, form, index):
        super(SubjectToTeacherBaseFormSet, self).add_fields(form, index)
        form.fields['teacher'] = forms.ModelChoiceField(queryset=Teacher.objects.all(), widget=LabelHiddenInput)


SubjectToTeacherInlineFormset = forms.models.inlineformset_factory(
    Subject,
    SubjectToTeacher,
    formset=SubjectToTeacherBaseFormSet,
    exclude=(),
    extra=2
)


class CoordinatorForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ('coordinator', )

    coordinator = forms.ModelChoiceField(queryset=Teacher.objects.all(), widget=LabelHiddenInput)
    delete = forms.BooleanField(required=False)

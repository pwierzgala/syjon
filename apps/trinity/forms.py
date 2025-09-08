"""
Created on 24-01-2012

@author: pwierzgala
"""


from django import forms

from apps.merovingian.models import Course, CourseToLeadingDiscipline
from apps.trinity.models import (
    CourseLearningOutcome, EducationArea, EducationDiscipline, EducationField,
    KnowledgeArea, ModuleLearningOutcome)

# ---------------------------------------------------
# --- LEADING DISCIPLINES
# ---------------------------------------------------

LeadingDisciplineInlineFormset = forms.models.inlineformset_factory(
    Course,
    CourseToLeadingDiscipline,
    exclude=('course',),
    max_num=1,
    extra=1
)


# ---------------------------------------------------
# --- EDUCATION AREAS
# ---------------------------------------------------

class EducationAreaForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('education_areas', )

    education_areas = forms.ModelMultipleChoiceField(
        queryset=EducationArea.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )


class EducationAreaPhdForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('knowledge_areas', 'education_fields', 'education_disciplines', )

    knowledge_areas = forms.ModelMultipleChoiceField(
        queryset=KnowledgeArea.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    education_fields = forms.ModelMultipleChoiceField(
        queryset=EducationField.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    education_disciplines = forms.ModelMultipleChoiceField(
        queryset=EducationDiscipline.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )


# ---------------------------------------------------
# --- COURSE LEARNING OUTCOMES
# ---------------------------------------------------

class CourseLearningOutcomeForm(forms.ModelForm):

    class Meta:
        model = CourseLearningOutcome
        fields = ('course', 'education_category', 'symbol', 'description', 'alos')
        widgets = {
            'course': forms.HiddenInput(),
            'education_category': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('queryset')
        widget = CheckboxSelectMultiple(learning_outcomes=queryset)
        super(CourseLearningOutcomeForm, self).__init__(*args, **kwargs)
        self.fields['alos'] = forms.ModelMultipleChoiceField(
            queryset=queryset,
            widget=widget,
            required=False
        )


class CourseLearningOutcomeLocsForm(forms.ModelForm):
    """
    Course Learning Outcomes form with Learning Outcomes Characteristics instead of
    Area Learning Outcomes.
    """

    class Meta:
        model = CourseLearningOutcome
        fields = ('course', 'education_category', 'symbol', 'description', 'locs')
        widgets = {
            'course': forms.HiddenInput(),
            'education_category': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('queryset')
        widget = CheckboxSelectMultiple(learning_outcomes=queryset)
        super(CourseLearningOutcomeLocsForm, self).__init__(*args, **kwargs)
        self.fields['locs'] = forms.ModelMultipleChoiceField(
            queryset=queryset,
            widget=widget,
            required=False
        )


# ---------------------------------------------------
# --- MODULE LEARNING OUTCOMES
# ---------------------------------------------------

class ModuleLearningOutcomeForm(forms.ModelForm):
    class Meta:
        model = ModuleLearningOutcome
        fields = ('module', 'symbol', 'description', 'clos')
        widgets = {'module': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('queryset')
        widget = CheckboxSelectMultiple(learning_outcomes=queryset)
        super(ModuleLearningOutcomeForm, self).__init__(*args, **kwargs)
        self.fields['clos'] = forms.ModelMultipleChoiceField(
            queryset=queryset,
            widget=widget,
            required=False
        )


# ---------------------------------------------------
# --- SUBJECT LEARNING OUTCOMES
# ---------------------------------------------------

class SubjectLearningOutcomesForm(forms.Form):

    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('queryset')
        widget = CheckboxSelectMultiple(learning_outcomes=queryset)
        super().__init__(*args, **kwargs)

        self.fields["mlos"] = forms.ModelMultipleChoiceField(
            queryset=queryset,
            widget=widget,
            required=False
        )


# ---------------------------------------------------
# --- WIDGETS
# ---------------------------------------------------

class CheckboxSelectMultiple(forms.SelectMultiple):
    template_name = 'trinity/form/learning_outcomes_select_multiple.html'

    def __init__(self, *args, **kwargs):
        self.learning_outcomes = kwargs.pop('learning_outcomes')
        super(CheckboxSelectMultiple, self).__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        ctx = super(CheckboxSelectMultiple, self).get_context(name, value, attrs)
        ctx['learning_outcomes'] = self.learning_outcomes
        ctx['value'] = [int(value) for value in ctx['value']]
        return ctx

import floppyforms.__future__ as forms
from django.utils.translation import ugettext_lazy as _

from apps.metacortex.models import (DidacticMethod, SyllabusModule,
                                    SyllabusPractice, SyllabusSubject)
from apps.metacortex.settings import (SYLLABUS_SEMESTER_CHOICES,
                                      SYLLABUS_TYPE_CHOICES,
                                      SYLLABUS_TYPE_SUBJECT_ID,
                                      SYLLABUS_YEAR_CHOICES)

# --------------------------------------------------------
# --- WIDGETS
# --------------------------------------------------------


class TextEditor(forms.Textarea):
    def __init__(self, *args, **kwargs):
        super(TextEditor, self).__init__(*args, **kwargs)
        self.attrs = {'class': 'ckeditor'}


class LearningOutcomesCheckboxSelectMultiple(forms.SelectMultiple):
    template_name = 'metacortex/form/widget/learning_outcomes_select_multiple.html'

    def __init__(self, *args, **kwargs):
        self.learning_outcomes = kwargs.pop('learning_outcomes')
        super(LearningOutcomesCheckboxSelectMultiple, self).__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        ctx = super(LearningOutcomesCheckboxSelectMultiple, self).get_context(name, value, attrs)
        ctx['learning_outcomes'] = self.learning_outcomes
        ctx['value'] = [int(value) for value in ctx['value']]
        return ctx


# -------------------------------------------------------
# --- FORMS
# -------------------------------------------------------

class SyllabusModuleForm(forms.ModelForm):
    class Meta:
        model = SyllabusModule
        exclude = ('coordinator', 'module', 'ectss', 'is_active', )
        widgets = {
            'module_description': TextEditor,
            'additional_information': TextEditor,
            'lecture_languages': forms.CheckboxSelectMultiple
        }


class SyllabusSubjectForm(forms.ModelForm):
    class Meta:
        model = SyllabusSubject
        exclude = ('teacher', 'subject', 'is_active')
        widgets = {
            'assessment_forms': forms.CheckboxSelectMultiple,
            'additional_information': TextEditor,
            'initial_requirements': TextEditor,
            'subjects_scope': TextEditor,
            'assessment_conditions': TextEditor,
            'learning_outcomes_verification': TextEditor,
            'literature': TextEditor,
            'education_effects': TextEditor
        }

    def __init__(self, *args, **kwargs):
        module_learning_outcomes_queryset = kwargs.pop('module_learning_outcomes')
        module_learning_outcomes_widget = LearningOutcomesCheckboxSelectMultiple(
            learning_outcomes=module_learning_outcomes_queryset
        )

        super(SyllabusSubjectForm, self).__init__(*args, **kwargs)

        self.fields['module_learning_outcomes'] = forms.ModelMultipleChoiceField(
            queryset=module_learning_outcomes_queryset,
            widget=module_learning_outcomes_widget,
            required=False,
            label=_('Module learning outcomes')
        )
        self.fields['didactic_methods'] = forms.ModelMultipleChoiceField(
            queryset=DidacticMethod.objects.visible(),
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )

    def clean_didactic_methods(self):
        data = self.cleaned_data['didactic_methods']
        if len(data) > 6:
            raise forms.ValidationError("Możesz wybrać do 6 pozycji.")
        return data


class SyllabusPracticeForm(forms.ModelForm):
    class Meta:
        model = SyllabusPractice
        exclude = ('teacher', 'subject', 'is_active')
        widgets = {
            'description': TextEditor,
            'additional_information': TextEditor,
            'education_effects': TextEditor,
        }


class SyllabusClassicSearchForm(forms.Form):
    """
    Klasyczny formularz wyszukiwania w wyszukiwarce sylabusów.
    """
       
    q = forms.CharField(widget=forms.TextInput, label=_(u"Search"), required=False)
    syllabus_type = forms.ChoiceField(
        widget=forms.Select,
        choices=SYLLABUS_TYPE_CHOICES,
        initial=SYLLABUS_TYPE_SUBJECT_ID,
        required=False
    )


class SearchForm(forms.Form):
    """
    Formularz wyszukiwania w zarządzaniu sylabusami.
    """
    name = forms.CharField(label='', required=False)


class SyllabusFilterForm(forms.Form):
    year = forms.ChoiceField(
        widget=forms.Select,
        choices=SYLLABUS_YEAR_CHOICES
    )
    semester = forms.ChoiceField(
        widget=forms.Select,
        choices=SYLLABUS_SEMESTER_CHOICES
    )
    type = forms.ChoiceField(
        widget=forms.Select,
        choices=SYLLABUS_TYPE_CHOICES,
        initial=SYLLABUS_TYPE_SUBJECT_ID,
        required=False
    )

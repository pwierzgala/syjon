from django import forms
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.merovingian.models import (DidacticOffer, Module, ModuleProperties,
                                     Subject)
from apps.merovingian.translation import (TranslatedInlineFormset,
                                          TranslatedModelForm)
from apps.trainman.models import Teacher

# ----------------------------------------------------------
# --- MODULE
# ----------------------------------------------------------

class LabelHiddenInput(forms.widgets.HiddenInput):
    def render(self, name, value, attrs=None):
        widget = super(LabelHiddenInput, self).render(name, value, attrs)
        label = str(Teacher.objects.get(id=int(value))) if value else u''
        return mark_safe(widget + u'<strong id="id_%s-label">' % (name) + label + u'</strong>')


class ModuleForm(TranslatedModelForm):
    class Meta:
        model = Module
        exclude = ('subjects', 'coordinator', 'sgroup', )


# ----------------------------------------------------------
# --- MODULE PROPERTIES
# ----------------------------------------------------------

class ModulePropertiesFormSet(forms.models.BaseInlineFormSet):
    def get_queryset(self):
        return super(ModulePropertiesFormSet, self).get_queryset()


ModulePropertiesInlineFormset = forms.models.inlineformset_factory(
    Module,
    ModuleProperties,
    exclude=(),
    formset=ModulePropertiesFormSet,
    extra=2,
    max_num=10
)


# ----------------------------------------------------------
# --- SUBJECT
# ----------------------------------------------------------

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        exclude = ('teachers', 'slos')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['ects_individual'].widget.attrs['readonly'] = True

    def save(self, commit=True):
        ects_all = self.instance.ects
        ects_classes = self.instance.ects_classes
        if ects_all is not None and ects_classes is not None:
            self.instance.ects_individual = ects_all - ects_classes
        return super().save(commit)


SubjectInlineFormset = forms.models.inlineformset_factory(
    Module,
    Subject,
    form=SubjectForm,
    extra=2
)


# ----------------------------------------------------------
# --- DIDACTIC OFFER
# ----------------------------------------------------------

class DidacticOfferForm(TranslatedModelForm):
    class Meta:
        model = DidacticOffer
        exclude = ()
        
    def __init__(self, *args, **kwargs):
        super(DidacticOfferForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget = forms.DateInput()
        self.fields['end_date'].widget = forms.DateInput()
        self.fields['start_date'].required = True
        self.fields['end_date'].required = True
        
    def clean(self):
        cleaned_data = super(DidacticOfferForm, self).clean()
    
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
    
        if start_date and end_date:
            if start_date > end_date:
                errors = self._errors.setdefault('start_date', ErrorList())
                errors.append(_(u'Start date cannot be later than end date')) 
            else:
                qs = DidacticOffer.objects
                if self.instance and self.instance.pk:
                    qs = qs.exclude(pk=self.instance.pk)
                doffers = qs.all()
                for doffer in doffers:
                    if doffer.start_date <= start_date <= doffer.end_date \
                            or doffer.start_date <= end_date <= doffer.end_date \
                            or start_date <= doffer.start_date <= end_date \
                            or start_date <= doffer.end_date <= end_date:
                        errors = self._errors.setdefault('start_date', ErrorList())
                        errors.append(_(u'The time period of teaching offer cannot overlap other offers')) 
                        break
        
        return cleaned_data

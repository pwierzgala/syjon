from modeltranslation.translator import (
    NotRegistered, TranslationOptions, translator)

from apps.trainman.models import (
    Department, DepartmentType, IdentityDocument, Occupation, TeacherDegree,
    TeacherPosition)
from syjon import settings


class DepartmentTranslationOptions(TranslationOptions):
    fields = ('name',)
class DepartmentTypeTranslationOptions(TranslationOptions):
    fields = ('name',)
class IdentityDocumentTranslationOptions(TranslationOptions):
    fields = ('name',)
class TeacherDegreeTranslationOptions(TranslationOptions):
    fields = ('name',)
class TeacherPositionTranslationOptions(TranslationOptions):
    fields = ('name',)
class OccupationTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Department, DepartmentTranslationOptions)
translator.register(DepartmentType, DepartmentTypeTranslationOptions)
translator.register(IdentityDocument, IdentityDocumentTranslationOptions)
translator.register(TeacherDegree, TeacherDegreeTranslationOptions)
translator.register(TeacherPosition, TeacherPositionTranslationOptions)
translator.register(Occupation, OccupationTranslationOptions)

from django import forms
from django.forms.utils import ErrorList
from django.utils import translation


class TranslatedInlineFormset(forms.models.BaseInlineFormSet):
    """
    This class fills in translated fields for each language with values 
    from original field or from instance if is provided.
    It is the equivalent of TranslatedModelForm for inline form sets.
    """
        
    def _populate_translation_fields(self):
        """
        """
        #Copy data to avoid immutable error 
        data_copy = self.data.copy() if self.data else None
        
        #Retrieve translation options if exist
        try:
            translation_options = translator.get_options_for_model(self.form._meta.model)
        except NotRegistered:
            translation_options = None
        
        instances = self.get_queryset().all()
        for i in xrange(self.total_form_count()):    
            
            prefix = self.add_prefix(i)
            instance = instances[i] if i < len(instances) else None
            
            #If data provided and model is translated
            if translation_options and data_copy:
                for field_name in translation_options.fields:
                    
                    # Save original name
                    original_field_name = field_name
                    # Get field name for current form
                    field_name = "%s-%s" % (prefix, field_name)
                    
                    # Copy main value to current language
                    # or copy the instance value to other languages if instance is not None
                    
                    if field_name in data_copy:
                        for lang_code, lang_name in settings.LANGUAGES:
                            if lang_code == translation.get_language():
                                data_copy[field_name+'_'+lang_code] = data_copy[field_name]
                            elif instance:
                                data_copy[field_name+'_'+lang_code] = getattr(instance, original_field_name+'_'+lang_code)
        self.data = data_copy
        

    def _construct_forms(self):
        """
        """
        self._populate_translation_fields()
        super(TranslatedInlineFormset, self)._construct_forms()
    

class TranslatedModelForm(forms.ModelForm):
    """
    This class fills in translated fields for each language with values 
    from original field or from instance if is provided.
    For contains only one field for each translated field and its value is copied
    to the field of current language.
    For other languages the value is copied from instance if it is not None. 
    """
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):
        
        #Copy data to avoid immutable error 
        data_copy = data.copy() if data else None
        
        #Retrieve translation options if exist
        try:
            translation_options = translator.get_options_for_model(self._meta.model)
        except NotRegistered:
            translation_options = None
        
        #If data provided and model is translated
        if translation_options and data_copy:
            for field_name in translation_options.fields:
                
                # Copy main value to current language
                # or copy the instance value to other languages if instance is not None
                if field_name in data_copy:
                    for lang_code, lang_name in settings.LANGUAGES:
                        if lang_code == translation.get_language():
                            data_copy[field_name+'_'+lang_code] = data_copy[field_name]
                        elif instance:
                            data_copy[field_name+'_'+lang_code] = getattr(instance, field_name+'_'+lang_code)
                    
        super(TranslatedModelForm, self).__init__(data_copy, files, auto_id, prefix,
                                                initial, error_class, label_suffix,
                                                empty_permitted, instance)
        
    
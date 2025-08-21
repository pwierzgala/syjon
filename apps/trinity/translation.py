from modeltranslation.translator import TranslationOptions, translator

from apps.trinity.models import (AreaLearningOutcome, CourseLearningOutcome,
                                 EducationArea, EducationCategory,
                                 EducationDiscipline, EducationField,
                                 KnowledgeArea, ModuleLearningOutcome)


class EducationAreaTranslationOptions(TranslationOptions):
    fields = ('name',)


class KnowledgeAreaTranslationOptions(TranslationOptions):
    fields = ('name',)


class EducationFieldTranslationOptions(TranslationOptions):
    fields = ('name',)


class EducationDisciplineTranslationOptions(TranslationOptions):
    fields = ('name',)


class EducationCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


class AreaLearningOutcomeTranslationOptions(TranslationOptions):
    fields = ('symbol', 'description')


class CourseLearningOutcomeTranslationOptions(TranslationOptions):
    fields = ('symbol', 'description')


class ModuleLearningOutcomeTranslationOptions(TranslationOptions):
    fields = ('symbol', 'description')  

translator.register(EducationArea, EducationAreaTranslationOptions)
translator.register(KnowledgeArea, KnowledgeAreaTranslationOptions)
translator.register(EducationField, EducationFieldTranslationOptions)
translator.register(EducationDiscipline, EducationDisciplineTranslationOptions)
translator.register(EducationCategory, EducationCategoryTranslationOptions)
translator.register(AreaLearningOutcome, AreaLearningOutcomeTranslationOptions)
translator.register(CourseLearningOutcome, CourseLearningOutcomeTranslationOptions)
translator.register(ModuleLearningOutcome, ModuleLearningOutcomeTranslationOptions)
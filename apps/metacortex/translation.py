from modeltranslation.translator import TranslationOptions, translator

from apps.metacortex.models import (ECTS, AssessmentForm, DidacticMethod,
                                    LectureLanguage, PracticeType,
                                    SyllabusModule, SyllabusPractice,
                                    SyllabusSubject)


class MetacortexSyllabusModuleTranslationOptions(TranslationOptions):
    fields = ('module_description', 'additional_information',)


class MetacortexSyllabusSubjectTranslationOptions(TranslationOptions):
    fields = ('additional_name', 'initial_requirements', 'literature',
              'subjects_scope', 'additional_information', 'education_effects')


class MetacortexSyllabusPracticeTranslationOptions(TranslationOptions):
    fields = ('description', 'education_effects', 'additional_information',)


class MetacortexECTSTranslationOptions(TranslationOptions):
    fields = ('name', )


class MetacortexPracticeTypeTranslationOptions(TranslationOptions):
    fields = ('name', )


class MetacortexLectureLanguageTranslationOptions(TranslationOptions):
    fields = ('name', )


class MetacortexDidacticMethodTranslationOptions(TranslationOptions):
    fields = ('name', )


class MetacortexAssessmentFormTranslationOptions(TranslationOptions):
    fields = ('name', )


translator.register(SyllabusModule, MetacortexSyllabusModuleTranslationOptions)
translator.register(SyllabusSubject, MetacortexSyllabusSubjectTranslationOptions)
translator.register(SyllabusPractice, MetacortexSyllabusPracticeTranslationOptions)
translator.register(ECTS, MetacortexECTSTranslationOptions)
translator.register(PracticeType, MetacortexPracticeTypeTranslationOptions)
translator.register(LectureLanguage, MetacortexLectureLanguageTranslationOptions)
translator.register(DidacticMethod, MetacortexDidacticMethodTranslationOptions)
translator.register(AssessmentForm, MetacortexAssessmentFormTranslationOptions)

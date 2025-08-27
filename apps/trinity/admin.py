# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.merovingian.models import Course
from apps.trinity.models import (AreaLearningOutcome, EducationArea,
                                 EducationCategory, EducationDiscipline,
                                 EducationField, KnowledgeArea,
                                 LeadingDiscipline, LearningOutcomeAspect,
                                 LearningOutcomeCharacteristic,
                                 LearningOutcomesEvaluation, TrinityProfile)


class TrinityProfileAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'get_email', 'get_courses')
    search_fields = ('^user_profile__user__last_name', '^user_profile__user__username')
    ordering = ('user_profile__user__last_name',)

    filter_vertical = ('courses',)

    def get_email(self, obj):
        return obj.user_profile.user.email
    get_email.short_description = _(u'Email')
    
    def get_courses(self, obj):
        result = ''
        for m in obj.courses.all():
            result += str(m) + '; '
        return result
    get_courses.short_description = _(u'Courses')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'courses':
            kwargs['queryset'] = Course.objects.all()
        return super(TrinityProfileAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


class AreaLearningOutcomeAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'education_level', 'education_area',
                    'education_profile', 'education_category')
    search_fields = ('^symbol',)
    ordering = ('education_level', 'education_area', 'education_profile',
                'education_category', 'symbol')


class LearningOutcomeCharacteristicAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'level', 'education_category', 'aspect')
    search_fields = ('^symbol',)
    ordering = ('level', 'education_category', 'symbol')


class LeadingDisciplineAdmin(admin.ModelAdmin):
    exclude = ('courses',)


class EducationAreaAdmin(admin.ModelAdmin):
    exclude = ('courses',)


class KnowledgeAreaAdmin(admin.ModelAdmin):
    exclude = ('courses',)


class EducationFieldAdmin(admin.ModelAdmin):
    exclude = ('courses',)


class EducationDisciplineAdmin(admin.ModelAdmin):
    exclude = ('courses',)



admin.site.register(TrinityProfile, TrinityProfileAdmin)

admin.site.register(LearningOutcomeAspect)
admin.site.register(AreaLearningOutcome, AreaLearningOutcomeAdmin)
admin.site.register(LeadingDiscipline, LeadingDisciplineAdmin)
admin.site.register(LearningOutcomeCharacteristic, LearningOutcomeCharacteristicAdmin)

admin.site.register(EducationArea, EducationAreaAdmin)
admin.site.register(EducationField, EducationFieldAdmin)
admin.site.register(EducationDiscipline, EducationDisciplineAdmin)
admin.site.register(EducationCategory)
admin.site.register(LearningOutcomesEvaluation)
admin.site.register(KnowledgeArea, EducationAreaAdmin)

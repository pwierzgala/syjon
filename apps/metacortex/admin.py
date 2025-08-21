# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from apps.metacortex.models import (ECTS, AssessmentForm, DidacticMethod,
                                    LectureLanguage, PracticeType,
                                    SyllabusModule, SyllabusSubject,
                                    SyllabusYear)


class SyllabusModuleAdmin(admin.ModelAdmin):
    list_display = ('module', 'get_coordinator', 'is_published', 'is_active')
    search_fields = ('^module__name',)
    exclude = ('module', 'coordinator')

    def get_coordinator(self, obj):
        return obj.coordinator
    get_coordinator.short_description = _(u'Coordinator')


class SyllabusSubjectAdmin(admin.ModelAdmin):
    search_fields = ('^subject__name',)
    list_display = ('subject', 'get_module', 'get_teacher', 'is_published', 'is_active')
    exclude = ('teacher', 'subject')
    
    def get_module(self, obj):
        return obj.subject.module
    get_module.short_description = _(u'Module')
    
    def get_teacher(self, obj):
        return obj.teacher
    get_teacher.short_description = _(u'Teacher')


class SyllabusYearAdmin(admin.ModelAdmin):
    list_display = ('get_date', 'read_only')
    
    def get_date(self, obj):
        return obj.date.year
    get_date.short_description = _(u'Year')


class EctsAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "flag", )
    list_filter = ('flag', )


class DidacticMethodAdmin(admin.ModelAdmin):
    list_display = ("name", "is_visible", "order", )
    list_filter = ('is_visible', )


admin.site.register(LectureLanguage)
admin.site.register(DidacticMethod, DidacticMethodAdmin)
admin.site.register(AssessmentForm)
admin.site.register(ECTS, EctsAdmin)
admin.site.register(SyllabusModule, SyllabusModuleAdmin)
admin.site.register(SyllabusSubject, SyllabusSubjectAdmin)
admin.site.register(PracticeType)
admin.site.register(SyllabusYear, SyllabusYearAdmin)

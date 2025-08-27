# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.merovingian.models import (Course, CourseLevel, CourseProfile,
                                     CourseType, DidacticOffer,
                                     MerovingianAdmin, MerovingianSettings,
                                     Module, ModuleProperties, ModuleType,
                                     SGroup, SGroupType, Subject,
                                     SubjectAssessment, SubjectType)


class MerovingianAdminAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'get_email', 'get_courses')
    search_fields = ('^user_profile__user__last_name',
                     '^user_profile__user__username')
    ordering = ('user_profile__user__last_name',)

    filter_vertical = ('courses',)

    def get_email(self, obj):
        return obj.user_profile.user.email
    get_email.short_description = _(u'email')

    def get_courses(self, obj):
        result = ''
        for m in obj.courses.all():
            result += str(m) + '; '
        return result
    get_courses.short_description = _(u'courses')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'level', 'type', 'profile',
                    'is_active')
    search_fields = ('^name',)
    ordering = ('name', '-level__name', '-type__name')


class SGroupAdmin(admin.ModelAdmin):
    fields = ('is_active', 'name', 'type', 'course', 'sgroup',
              'start_semester', 'didactic_offer',)
    list_display = ('course', 'name', 'type')
    search_fields = ('^course__name', '^name')
    ordering = ('course__name', )


class ModuleAdmin(admin.ModelAdmin):
    search_fields = ('^name', )
    list_display = ('name', 'sgroup', 'get_course')

    def get_course(self, obj):
        return None if obj.sgroup is None else obj.sgroup.course
    get_course.short_description = _(u'Course')


class DidacticOfferAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active')


admin.site.register(MerovingianSettings)
admin.site.register(MerovingianAdmin, MerovingianAdminAdmin)
admin.site.register(DidacticOffer, DidacticOfferAdmin)
admin.site.register(CourseLevel)
admin.site.register(CourseType)
admin.site.register(CourseProfile)
admin.site.register(Course, CourseAdmin)
admin.site.register(SGroupType)
admin.site.register(SGroup, SGroupAdmin)
admin.site.register(SubjectType)
admin.site.register(SubjectAssessment)
admin.site.register(ModuleType)
admin.site.register(Module, ModuleAdmin)
admin.site.register(ModuleProperties)
admin.site.register(Subject)

# -*- coding: utf-8 -*-

from django.contrib import admin, auth, messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect
from django.urls import re_path, reverse
from django.utils.translation import gettext_lazy as _

from apps.trainman.backends import fake_authenticate
from apps.trainman.models import (
    Department, DepartmentType, IdentityDocument, Teacher, TeacherDegree,
    TeacherPosition, UserProfile)

# --------------------------------------------------
# --- AUTH
# --------------------------------------------------

class SyjonUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'get_department', 'login_column')
    
    staff_fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    def get_urls(self):
        urls = super(SyjonUserAdmin, self).get_urls()
        urls = [
            re_path(
                r'^login/(?P<user_id>\d+)/$',
                self.admin_site.admin_view(self.login_view),
                name='trainman_user_login')
        ] + urls
        return urls

    def login_column(self, obj):
        return '<a href="%s">%s</a>' % (
            reverse('admin:trainman_user_login', kwargs={'user_id': obj.id}),
            _(u'Log in'))
    login_column.short_description = _(u"Log in to user's account")
    login_column.allow_tags = True

    def get_department(self, obj):
        return obj.userprofile.department
    get_department.short_description = _(u'Wydział')

    def login_view(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
            admin_username = request.user.username
            
            login_user = fake_authenticate(user.username)
            auth.logout(request)
            auth.login(request, login_user)
            
            request.session['admin_username'] = admin_username
            if login_user:
                messages.success(request, _(u"Relogged successfully"))

            return redirect('syjon:home')
        except User.DoesNotExist:
            messages.error(request, _(u"Selected user does not exist"))
            return redirect('admin:auth_user_changelist')
    
    def change_view(self, request, *args, **kwargs):
        # for non-superuser
        if not request.user.is_superuser:
            try:
                self.fieldsets = self.staff_fieldsets
                response = UserAdmin.change_view(self, request, *args, **kwargs)
            finally:
                # Reset fieldsets to its original value
                self.fieldsets = UserAdmin.fieldsets
            return response
        else:
            return UserAdmin.change_view(self, request, *args, **kwargs)

    def get_queryset(self, request):
        queryset = super(SyjonUserAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.exclude(is_superuser=True)
        return queryset
            

admin.site.unregister(User)
admin.site.register(User, SyjonUserAdmin)


class SyjonGroupAdmin(admin.ModelAdmin):
    filter_vertical = ('permissions',)

admin.site.unregister(Group)
admin.site.register(Group, SyjonGroupAdmin)


# --------------------------------------------------
# --- TRAINMAN
# --------------------------------------------------

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('username', 'degree', 'position', 'department', )
    search_fields = ('user_profile__user__last_name', )
    list_filter = ('degree', 'position', )
    raw_id_fields = ('user_profile', )

    def username(self, obj):
        return obj.user_profile.user.get_full_name()
    username.short_description = _(u"Username")
    username.allow_tags = True

    def department(self, obj):
        return obj.user_profile.department
    department.short_description = _(u"Jednostka")
    department.allow_tags = True

    def get_queryset(self, request):
        queryset = super(TeacherAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.exclude(user_profile__user__is_superuser=True)

        return queryset


# --------------------------------------------------
# --- USER PROFILE 
# --------------------------------------------------

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'department',)
    search_fields = ('user__last_name',)
    raw_id_fields = ('user', )

    staff_fieldsets = (
        (None, {'fields': ('user', 'second_name', 'pesel', 'department')}),
    )

    def username(self, obj):
        return obj.user.get_full_name()
    username.short_description = _(u"Username")
    username.allow_tags = True

    def change_view(self, request, *args, **kwargs):
        # for non-superuser
        if request.user.is_superuser:
            return admin.ModelAdmin.change_view(self, request, *args, **kwargs)
        else:
            try:
                self.fieldsets = self.staff_fieldsets
                response = admin.ModelAdmin.change_view(self, request, *args, **kwargs)
            finally:
                # Reset fieldsets to its original value
                self.fieldsets = admin.ModelAdmin.fieldsets
            return response

    def get_queryset(self, request):
        queryset = super(UserProfileAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.exclude(user__is_superuser=True)
        return queryset

    
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(TeacherDegree)
admin.site.register(TeacherPosition)
admin.site.register(Department)
admin.site.register(DepartmentType)
admin.site.register(IdentityDocument)

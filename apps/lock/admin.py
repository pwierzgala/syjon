# -*- coding: utf-8 -*-

from django.contrib import admin

from apps.lock.models import (Item, ItemType, ItemUser, ItemUserType, Key,
                              LockAdmin, Property, Room, RoomType)


class ItemUserInlineAdmin(admin.TabularInline):
    model = ItemUser
    extra = 2
    can_delete = True
    raw_id_fields = ('user',)


class PropertyInlineAdmin(admin.TabularInline):
    model = Property
    can_delete = True
    fields = ('key', 'value', 'item')


class ItemTypeAdmin(admin.ModelAdmin):
    model = ItemType
    filter_vertical = ('keys',)


class ItemAdmin(admin.ModelAdmin):
    save_on_top = True
    save_as = True
    list_display = ('name', 'type', 'serial_number', 'inventory_number', 'room', 'price', 'get_users', 'is_verified')
    list_filter = ('type', 'is_verified')
    search_fields = ('^name', '^serial_number', '^inventory_number', '^room__name', '^users__user__last_name')
    raw_id_fields = ('item',)
    inlines = (
        ItemUserInlineAdmin, 
        PropertyInlineAdmin,
        )

    def get_queryset(self, request):
        if not request.user.is_superuser:
            try:
                lock_admin = LockAdmin.objects.get(user_profile=request.user.userprofile)
                return super(ItemAdmin, self).get_queryset(request).filter(room__department__in=lock_admin.departments.all())
            except LockAdmin.DoesNotExist:
                return Item.objects.none()
        return super(ItemAdmin, self).get_queryset(request)
            
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'room' and not request.user.is_superuser:
            try:
                lock_admin = LockAdmin.objects.get(user_profile=request.user.userprofile)
                kwargs['queryset'] = Room.objects.filter(department__in=lock_admin.departments.all())
            except LockAdmin.DoesNotExist:
                kwargs['queryset'] = Room.objects.none()
        elif db_field.name == 'item' and not request.user.is_superuser:
            try:
                lock_admin = LockAdmin.objects.get(user_profile=request.user.userprofile)
                kwargs['queryset'] = Item.objects.filter(room__department__in=lock_admin.departments.all())
            except LockAdmin.DoesNotExist:
                kwargs['queryset'] = Item.objects.none()
        return super(ItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_formsets(self, request, obj=None):
        for inline in self.get_inline_instances(request):
            if isinstance(inline, PropertyInlineAdmin) and obj is None:
                continue
            yield inline.get_formset(request, obj)

    def get_users(self, obj):
        result = ''
        for user in obj.users.all():
            result += '%s - %s; ' % (str(user), str(ItemUser.objects.filter(
                item__exact=obj,
                user__exact=user)[0].type)
            )
        return result
    get_users.short_description = 'Użytkownicy'


class LockAdminAdmin(admin.ModelAdmin):
    model = LockAdmin
    filter_vertical = ('departments',)

admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemUserType)
admin.site.register(Key)
admin.site.register(LockAdmin, LockAdminAdmin)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import UserProfile

# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    def _username(self, obj):
        return obj.user.username
    _username.short_description = 'username'

    def _lastlogin(self, obj):
        return obj.user.last_login
    _lastlogin.short_description = 'Last Login at'

    def _active(self, obj):
        return obj.user.is_active
    _active.short_description = 'active'
    list_display = (
            '_username',
            'id',
            '_active',
            '_lastlogin',
            )
    list_filter = (
           )
    search_fields = (
            )
    readonly_fields = (
            )


admin.site.register(UserProfile, UserProfileAdmin)

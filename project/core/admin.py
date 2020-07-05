from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from core import models


# Django comes with a admin interface you can customize to some level
# This file allows you customize how the admin form will look like in
# your browser.
# Here I'm deciding what fields to show. All these fields come from the
# base admin class for user, except partner that was added to the model.
# See models.py
# Note: See the last line of code , the registration of this class, where
# we register the model User to this Admin form.


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name', 'partner',]
    # Each of the brackets is a section
    # first argument is the title
    # Note the ('name',) the comma is so python doesn't think
    # it is just a string but an array/tuple?
    # the _('blah') is what? something about json??
    fieldsets = (
        (None, {'fields': ('email', 'password', 'partner',)}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Import dates'), {'fields': ('last_login',)})
    )

    add_fieldsets = (
        (None, {'classes': ('wide', ),
                'fields': ('email', 'partner', 'password1', 'password2')
                }),
    )


admin.site.register(models.User, UserAdmin)

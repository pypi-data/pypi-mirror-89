from unchained_auth.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import Group


admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ["__str__", 'email']
    list_filter = ()
    search_fields = ()
    ordering = ()
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', )}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'groups'),
        }),
    )

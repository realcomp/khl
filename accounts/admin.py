from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import UsrChngForm, UsrCrtForm
from .models import User


class UserAdmin(DefaultUserAdmin):
    form = UsrChngForm
    add_form = UsrCrtForm
    #readonly_fields = 'username', 'email'
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'fio',
            'is_active',
            'avatar',
        )}),
        (_('Permissions'), {'fields': ('is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'username', 'password1', 'password2', 'fio'),
        }),
    )
    list_display= ( 'id', 'fio', 'username',  'is_staff', 'is_active',)
    list_filter = ( 'is_staff', 'is_superuser', 'is_active',
                    'groups', 'fio',)
    ordering = '-id',
admin.site.register(User, UserAdmin)

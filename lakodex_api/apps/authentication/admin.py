from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

from lakodex_api.apps.profiles.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    readonly_fields = ('created_at', 'updated_at',)
    can_delete = False
    verbose_name_plural = 'Profile'
    # fk_name = 'user'


class CustomUserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline, ]


# admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.user.models import User

# Register your models here.

class CustomUser(UserAdmin):
    # adjustments
    fieldsets = UserAdmin.fieldsets + (
            ('Extra Fields', {'fields': ('title', 'bio')}),
    )

    
admin.site.register(User, CustomUser)
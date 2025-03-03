from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Job, Application  # Import your models


# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('User Type', {'fields': ('user_type',)}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Job)
admin.site.register(Application)


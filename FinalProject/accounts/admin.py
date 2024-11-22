from django.contrib import admin

from FinalProject.accounts.models import Profile


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_student', 'first_name', 'last_name', 'profile_picture']

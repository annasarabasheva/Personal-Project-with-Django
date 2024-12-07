from django.contrib import admin
from django.contrib.auth import get_user_model
from FinalProject.accounts.models import Profile


UserModel = get_user_model()


@admin.register(UserModel)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'get_is_student', 'get_date_joined')
    ordering = ['username']
    readonly_fields = ['get_is_student', 'get_date_joined']

    def get_is_student(self, obj):
        return obj.profile.is_student

    get_is_student.short_description = 'Is Student'

    def get_date_joined(self, obj):
        return obj.date_joined

    get_date_joined.short_description = 'Date Joined'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_student', 'first_name', 'last_name', 'profile_picture']
    ordering = ['user']
    list_filter = ['is_student']
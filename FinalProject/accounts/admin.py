from django.contrib import admin
from django.contrib.auth import get_user_model
from FinalProject.accounts.models import Profile


UserModel = get_user_model()


@admin.register(UserModel)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    ordering = ['username']
    search_fields = ['username', 'email']
    list_filter = ['is_staff', 'is_superuser']

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return request.user.has_perm('auth.view_user')

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return request.user.has_perm('auth.change_user')

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_student', 'first_name', 'last_name', 'profile_picture']
    ordering = ['user']
    list_filter = ['is_student']

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return request.user.has_perm('accounts.view_profile')

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return request.user.has_perm('accounts.change_profile')

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False  # Students shouldn't delete profiles

    def has_add_permission(self, request):
        return request.user.is_superuser

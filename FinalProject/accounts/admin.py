from django.contrib import admin
from django.contrib.auth import get_user_model
from FinalProject.accounts.models import Profile

# Register the custom user model (AppUser) in the admin
UserModel = get_user_model()


@admin.register(UserModel)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'get_is_student')  # Show 'username' and 'is_student'

    def get_is_student(self, obj):
        return obj.profile.is_student  # Access `is_student` through the `profile`
    get_is_student.short_description = 'Is Student'


# Register Profile model
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_student', 'first_name', 'last_name', 'profile_picture']

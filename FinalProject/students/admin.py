from django.contrib import admin
from .models import Student


class StudentAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        # Allow staff users to see all students but restrict editing to their own profile
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs

    def has_change_permission(self, request, obj=None):
        # Allow editing only if the student profile belongs to the logged-in user
        if obj is not None and obj.profile.user != request.user:
            return False
        return super().has_change_permission(request, obj)


admin.site.register(Student, StudentAdmin)

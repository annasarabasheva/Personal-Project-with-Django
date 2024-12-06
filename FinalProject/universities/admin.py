from django.contrib import admin
from .models import University


class UniversityAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        # Allow staff users to see all universities but restrict editing to their own created ones
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs

    def has_change_permission(self, request, obj=None):
        # Allow editing only if the university was created by the logged-in user
        if obj is not None and obj.created_by != request.user:
            return False
        return super().has_change_permission(request, obj)


admin.site.register(University, UniversityAdmin)

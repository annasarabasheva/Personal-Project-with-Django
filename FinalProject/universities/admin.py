from django.contrib import admin
from FinalProject.universities.models import University


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'country', 'created_by']
    ordering = ['name']
    list_filter = ['created_by']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.created_by != request.user:
            return False

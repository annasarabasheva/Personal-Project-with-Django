from django.contrib import admin
from FinalProject.universities.models import University


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'country', 'get_created_by', 'year_established']
    ordering = ['name']
    list_filter = ['country', 'city', 'year_established']
    search_fields = ['name', 'city', 'country']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'country', 'city', 'logo_url', 'year_established'),
        }),
        ('Administrative Details', {
            'fields': ('created_by',),
        }),
    )

    list_display_links = ['name']

    def get_created_by(self, obj):
        return obj.created_by.username if obj.created_by else "Not Assigned"

    get_created_by.short_description = 'Created By'

    readonly_fields = ['year_established']
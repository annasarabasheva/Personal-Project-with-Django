from django.contrib import admin
from FinalProject.students.models import Student, Message, Rating


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'field_of_study', 'get_university', 'year_of_study',
                    'get_average_rating']
    ordering = ['first_name', 'last_name']
    list_filter = ['university', 'field_of_study', 'year_of_study']
    search_fields = ['first_name', 'last_name', 'field_of_study', 'university__name']

    fieldsets = (
        ('Basic Information', {
            'fields': ('first_name', 'last_name', 'photo', 'bio'),
        }),
        ('Academic Details', {
            'fields': ('university', 'field_of_study', 'year_of_study', 'location'),
        }),
        ('Profile Link', {
            'fields': ('profile',),
        }),
    )

    list_display_links = ['first_name', 'last_name']

    def get_university(self, obj):
        return obj.university.name if obj.university else "Not Assigned"

    get_university.short_description = 'University'

    def get_average_rating(self, obj):
        return round(obj.average_rating(), 2)

    get_average_rating.short_description = 'Average Rating'

    readonly_fields = ['profile']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'student', 'timestamp', 'parent_message', 'content_preview')
    search_fields = ('sender__username', 'student__first_name', 'student__last_name', 'content')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)

    def content_preview(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    content_preview.short_description = 'Content Preview'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('student', 'user', 'stars', 'created_at')
    ordering = ('-created_at',)
    list_filter = ('stars', 'created_at')
    search_fields = ('student__first_name', 'student__last_name', 'user__username')

    fieldsets = (
        ('Rating Details', {
            'fields': ('student', 'user', 'stars'),
        }),
        ('Timestamps', {
            'fields': ('created_at',),
        }),
    )
    readonly_fields = ('created_at',)
from django.contrib import admin
from FinalProject.students.models import Student, Message


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'university', 'field_of_study', 'year_of_study')
    search_fields = ('first_name', 'last_name', 'field_of_study')
    list_filter = ('university', 'year_of_study')
    ordering = ('first_name', 'last_name')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(profile__user=request.user)

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.profile.user != request.user:
            return False
        return super().has_change_permission(request, obj)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'student', 'timestamp', 'parent_message', 'content_preview')
    search_fields = ('sender__username', 'student__first_name', 'student__last_name', 'content')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)

    def content_preview(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    content_preview.short_description = 'Content Preview'
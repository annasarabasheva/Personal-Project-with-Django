from django.contrib import admin
from FinalProject.students.models import Student, Message


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'field_of_study', 'university']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.is_staff:
            return qs.filter(profile__user=request.user)
        return qs.none()


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'student', 'timestamp', 'parent_message', 'content_preview')
    search_fields = ('sender__username', 'student__first_name', 'student__last_name', 'content')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)

    def content_preview(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    content_preview.short_description = 'Content Preview'
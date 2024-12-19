from django.contrib import admin
from FinalProject.forum.models import Thread, Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'thread_count')
    search_fields = ('name', 'description')
    ordering = ('name',)
    list_filter = ('name',)

    def thread_count(self, obj):
        return obj.thread_set.count()

    thread_count.short_description = 'Thread Count'


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'updated_at', 'post_count')
    ordering = ('-created_at',)
    list_filter = ('category', 'author', 'created_at')
    search_fields = ('title', 'author__username', 'category__name')
    date_hierarchy = 'created_at'

    def post_count(self, obj):
        return obj.posts.count()

    post_count.short_description = 'Post Count'

    fieldsets = (
        ('Thread Details', {
            'fields': ('title', 'author', 'category')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'thread', 'like_count', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    list_filter = ('thread', 'author', 'created_at')
    search_fields = ('content', 'author__username', 'thread__title')

    fieldsets = (
        ('Post Details', {
            'fields': ('thread', 'author', 'content')
        }),
        ('Engagement', {
            'fields': ('likes',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
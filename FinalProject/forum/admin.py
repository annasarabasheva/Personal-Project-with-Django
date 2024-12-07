from django.contrib import admin
from FinalProject.forum.models import Thread, Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)
    list_filter = ('name',)


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'author')
    search_fields = ('title', 'author__username', 'category__name')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'thread', 'content', 'created_at', 'updated_at')
    list_filter = ('thread', 'author')
    search_fields = ('content', 'author__username', 'thread__title')
    ordering = ('-created_at',)
    list_editable = ('content',)
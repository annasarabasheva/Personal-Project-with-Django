from django.contrib import admin

from FinalProject.forum.models import Thread, Category, Post


# Register your models here.
@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
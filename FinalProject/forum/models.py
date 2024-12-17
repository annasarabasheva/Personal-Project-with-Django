from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User

UserModel = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Thread(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(UserModel, related_name="liked_posts", blank=True)

    def like_count(self):
        return self.likes.count()

    def __str__(self):
        return f"Post by {self.author} in {self.thread.title}"


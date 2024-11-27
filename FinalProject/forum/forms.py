from django import forms
from .models import Thread, Post, Category


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'category']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
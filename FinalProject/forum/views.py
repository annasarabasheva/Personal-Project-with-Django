from django.shortcuts import render, get_object_or_404, redirect

from FinalProject.forum.forms import PostForm, ThreadForm, CategoryForm
from FinalProject.forum.models import Category, Thread


def forum_home(request):
    categories = Category.objects.all()
    threads = Thread.objects.order_by('-updated_at')[:10]
    return render(request, 'forum/forum-home.html', {'categories': categories, 'threads': threads})


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    threads = category.thread_set.order_by('-updated_at')
    return render(request, 'forum/category-detail.html', {'category': category, 'threads': threads})


def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    posts = thread.posts.all()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.thread = thread
            post.save()
            return redirect('thread-detail', thread_id=thread.id)
    else:
        form = PostForm()
    return render(request, 'forum/thread-detail.html', {'thread': thread, 'posts': posts, 'form': form})


def create_thread(request):
    if request.method == "POST":
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            return redirect('thread-detail', thread_id=thread.id)
    else:
        form = ThreadForm()
    return render(request, 'forum/create-thread.html', {'form': form})


def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('forum-home')  # Redirect to the forum home page after creating the category
    else:
        form = CategoryForm()

    return render(request, 'forum/create-category.html', {'form': form})
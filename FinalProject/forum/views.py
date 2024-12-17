from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, CreateView
from FinalProject.forum.forms import PostForm, ThreadForm, CategoryForm
from FinalProject.forum.models import Category, Thread, Post


class ForumHomeView(TemplateView):
    template_name = 'forum/forum-home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['threads'] = Thread.objects.order_by('-updated_at')[:10]
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'forum/category-detail.html'
    context_object_name = 'category'
    pk_url_kwarg = 'category_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['threads'] = self.object.thread_set.order_by('-updated_at')
        return context


class ThreadDetailView(DetailView):
    model = Thread
    template_name = 'forum/thread-detail.html'
    context_object_name = 'thread'
    pk_url_kwarg = 'thread_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.all()
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.thread = self.object
            post.save()
            return redirect('thread-detail', thread_id=self.object.id)
        return self.render_to_response(self.get_context_data(form=form))


class CreateThreadView(LoginRequiredMixin, CreateView):
    model = Thread
    form_class = ThreadForm
    template_name = 'forum/create-thread.html'

    def form_valid(self, form):
        thread = form.save(commit=False)
        thread.author = self.request.user
        thread.save()
        return redirect('thread-detail', thread_id=thread.id)


class CreateCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'forum/create-category.html'
    success_url = reverse_lazy('forum-home')


def like_post(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'You must be logged in to like a post.'}, status=403)

    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)  # Unlike
        liked = False
    else:
        post.likes.add(request.user)  # Like
        liked = True

    return JsonResponse({'liked': liked, 'like_count': post.like_count()})
from django.urls import path
from FinalProject.forum.views import ForumHomeView, CategoryDetailView, ThreadDetailView, CreateThreadView, \
    CreateCategoryView, like_post, ThreadEditView, ThreadDeleteView

urlpatterns = [
    path('', ForumHomeView.as_view(), name='forum-home'),
    path('category/<int:category_id>/', CategoryDetailView.as_view(), name='category-detail'),
    path('thread/<int:thread_id>/', ThreadDetailView.as_view(), name='thread-detail'),
    path('thread/create/', CreateThreadView.as_view(), name='create-thread'),
    path('thread/<int:pk>/edit/', ThreadEditView.as_view(), name='thread-edit'),
    path('thread/<int:pk>/delete/', ThreadDeleteView.as_view(), name='thread-delete'),
    path('category/create/', CreateCategoryView.as_view(), name='create-category'),
    path('post/<int:post_id>/like/', like_post, name='like-post'),
]

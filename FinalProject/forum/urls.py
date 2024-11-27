from django.urls import path

from FinalProject.forum import views

urlpatterns = [
    path('', views.forum_home, name='forum-home'),
    path('category/<int:category_id>/', views.category_detail, name='category-detail'),
    path('thread/<int:thread_id>/', views.thread_detail, name='thread-detail'),
    path('thread/create/', views.create_thread, name='create-thread'),
    path('category/create/', views.create_category, name='create-category'),
]

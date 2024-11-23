from django.urls import path
from FinalProject.universities import views

urlpatterns = [
    path('catalog/', views.catalog, name='catalog'),
    path('all-unis/', views.all_unis, name='all-unis'),
    path('add-university/', views.add_university, name='add-university'),
    path('edit-university/', views.edit_university, name='edit-university'),
    path('delete-university/', views.delete_university, name='delete-university'),
    path('my-university/', views.my_university, name='my-university'),
]
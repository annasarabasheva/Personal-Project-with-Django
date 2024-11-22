from django.urls import path
from FinalProject.universities import views

urlpatterns = [
    path('catalog/', views.catalog, name='catalog'),
    path('all_unis/', views.all_unis, name='all-unis'),
    path('add-university/', views.add_university, name='add-university'),
]
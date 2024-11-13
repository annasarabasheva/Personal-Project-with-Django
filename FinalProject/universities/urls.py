from django.urls import path
from FinalProject.universities import views

urlpatterns = [
    path('catalog/', views.catalog, name='catalog'),
]
from django.urls import path
from FinalProject.students import views

urlpatterns = [
    path('university/<int:university_id>/', views.university_students, name='university_students'),
]
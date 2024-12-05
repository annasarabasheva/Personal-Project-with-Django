from django.urls import path
from FinalProject.students import views


urlpatterns = [
    path('university/<int:university_id>/', views.university_students, name='university_students'),
    path('student/<int:student_id>/', views.student_detail, name='student-detail'),
    path('student-form/', views.student_form_view, name='student-form'),
    path('<int:student_id>/edit/', views.student_edit, name='student-edit'),
    path('<int:student_id>/delete/', views.student_delete, name='student-delete'),
]
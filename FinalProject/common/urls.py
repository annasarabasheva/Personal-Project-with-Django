from django.urls import path
from FinalProject.common import views


urlpatterns = [
    path('', views.home_page, name='home'),

]
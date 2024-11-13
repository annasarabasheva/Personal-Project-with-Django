from django.contrib.auth.views import LogoutView
from django.urls import path
from FinalProject.accounts.views import AppUserLoginView, AppUserRegisterView
urlpatterns = [
    path('login/', AppUserLoginView.as_view(), name='login'),
    path('register/', AppUserRegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout')

]
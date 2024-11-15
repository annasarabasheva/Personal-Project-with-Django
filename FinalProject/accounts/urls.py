from django.contrib.auth.views import LogoutView
from django.urls import path, include
from FinalProject.accounts.views import AppUserLoginView, AppUserRegisterView, my_profile, edit_profile

urlpatterns = [
    path('login/', AppUserLoginView.as_view(), name='login'),
    path('register/', AppUserRegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', include([
        path('', my_profile, name='profile-details'),
        path('edit/', edit_profile, name='profile-edit'),
    ]))

]
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from FinalProject.accounts.views import AppUserLoginView, AppUserRegisterView, ProfileDetailView, ProfileEditView, \
    ProfileDeleteView

urlpatterns = [
    path('login/', AppUserLoginView.as_view(), name='login'),
    path('register/', AppUserRegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', include([
        path('', ProfileDetailView.as_view(), name='profile-details'),
        path('edit/', ProfileEditView.as_view(), name='profile-edit'),
        path('delete/', ProfileDeleteView.as_view(), name='profile-delete')
    ]))

]
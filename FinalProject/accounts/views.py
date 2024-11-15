from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from FinalProject.accounts.forms import AppUserCreationForm
from FinalProject.accounts.models import Profile

UserModel = get_user_model()


class AppUserLoginView(LoginView):
    template_name = 'accounts/login-page.html'


class AppUserRegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)

        login(self.request, self.object)  # Auto Login after Register

        return response


def my_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    profile = get_object_or_404(Profile, user=request.user)

    context = {
        'profile': profile,
    }
    return render(request, 'accounts/profile-details-page.html', context)
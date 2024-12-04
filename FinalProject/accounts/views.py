from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from FinalProject.accounts.forms import AppUserCreationForm, ProfileEditForm
from FinalProject.accounts.models import Profile

UserModel = get_user_model()


class AppUserLoginView(LoginView):
    template_name = 'accounts/login-page.html'
    next_page = reverse_lazy('all-unis')


class AppUserRegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('all-unis')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Auto Login after Register
        login(self.request, self.object)

        # Update profile `is_student` value
        profile = self.object.profile
        profile.is_student = form.cleaned_data.get('is_student', False)
        profile.save()

        if profile.is_student:
            return redirect('student-form')

        return response


def my_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    profile = get_object_or_404(Profile, user=request.user)

    context = {
        'profile': profile,
    }
    return render(request, 'accounts/profile-details-page.html', context)


@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile-details')  # Adjust this to your actual profile detail URL
    else:
        form = ProfileEditForm(instance=profile)

    context = {
        'form': form,
    }
    return render(request, 'accounts/profile-edit-page.html', context)


@login_required
def delete_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST' and 'confirm' in request.POST:
        user = request.user
        profile.delete()
        user.delete()

        logout(request)
        messages.success(request, "Your profile has been successfully deleted.")
        return redirect('home')

    return render(request, 'accounts/profile-delete-page.html')
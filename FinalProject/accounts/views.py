from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView
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

        # Auto-login after registration
        login(self.request, self.object)

        # Update profile `is_student` value
        profile = self.object.profile
        profile.is_student = form.cleaned_data.get('is_student', False)
        profile.save()

        if profile.is_student:
            self.object.is_staff = True
            self.object.save()

            # Add the user to the "Student Group"
            student_group, created = Group.objects.get_or_create(name='Student Group')
            self.object.groups.add(student_group)

            # Redirect to student form if the user registers as a student
            return redirect('student-form')

        return response


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile-details-page.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit-page.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def get_success_url(self):
        return reverse('profile-details')


class ProfileDeleteView(LoginRequiredMixin, View):
    template_name = 'accounts/profile-delete-page.html'

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if 'confirm' in request.POST:
            profile = self.get_object()
            user = request.user
            profile.delete()
            user.delete()

            logout(request)
            messages.success(request, "Your profile has been successfully deleted.")
            return redirect('home')
        return render(request, self.template_name)
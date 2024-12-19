from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.db import transaction

from FinalProject.accounts.models import Profile

UserModel = get_user_model()


class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel


class AppUserCreationForm(UserCreationForm):
    is_student = forms.BooleanField(
        required=False,
        label="Are you a student?",
        help_text="Check this if you are currently a student."
    )

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('email', 'username')

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()

            profile, created = Profile.objects.get_or_create(user=user)

            profile.is_student = self.cleaned_data.get('is_student', False)

            print(f"Saving profile for user {user.username}: is_student={profile.is_student}")

            profile.save()

        return user


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'profile_picture']

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'profile_picture': forms.URLInput(attrs={'placeholder': 'Profile Picture URL'}),
        }
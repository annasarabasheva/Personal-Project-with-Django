from django import forms
from django.core.exceptions import ValidationError

from FinalProject.universities.models import University


from django import forms
from FinalProject.universities.models import University


class UniversityForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ['name', 'country', 'city', 'logo_url', 'year_established']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'University Name'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'logo_url': forms.URLInput(attrs={'placeholder': 'Logo URL'}),
            'year_established': forms.NumberInput(attrs={'placeholder': 'Year Established'}),
        }

    def clean_year_established(self):
        year_established = self.cleaned_data.get('year_established')
        if year_established and year_established < 1000:
            raise forms.ValidationError('Year of establishment must be a valid year.')
        return year_established


class UniversitySelectionForm(forms.Form):
    existing_university = forms.ModelChoiceField(
        queryset=University.objects.all(),
        required=False,
        empty_label="-- Check if we already have your university in our database --",
        label="Existing University",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    new_university_name = forms.CharField(
        max_length=150,
        required=False,
        label="Your University Name",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your university name if it was not in our database', 'class': 'form-control'}),
    )
    country = forms.CharField(
        max_length=100,
        required=False,
        label="Country",
        widget=forms.TextInput(attrs={'placeholder': 'Country...', 'class': 'form-control'}),
    )
    city = forms.CharField(
        max_length=100,
        required=False,
        label="City",
        widget=forms.TextInput(attrs={'placeholder': 'City...', 'class': 'form-control'}),
    )

    year_established = forms.IntegerField(
        required=False,
        label="Year Established",
        widget=forms.NumberInput(attrs={'placeholder': 'Year Established...', 'class': 'form-control'})
    )

    logo_url = forms.URLField(
        required=False,
        label="Logo URL",
        widget=forms.URLInput(attrs={'placeholder': 'Logo URL of your university...', 'class': 'form-control'})
    )

    def clean_new_university_name(self):
        new_university_name = self.cleaned_data.get('new_university_name')
        if new_university_name and University.objects.filter(name=new_university_name).exists():
            raise ValidationError(f"A university with the name '{new_university_name}' already exists in our database.")
        return new_university_name

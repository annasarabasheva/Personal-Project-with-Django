from django import forms
from FinalProject.universities.models import University


class UniversityForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ['name', 'country', 'city', 'description', 'logo_url', 'year_established']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'University Name'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'description': forms.Textarea(attrs={'placeholder': 'Short description of the university'}),
            'logo_url': forms.URLInput(attrs={'placeholder': 'Logo URL'}),
            'year_established': forms.NumberInput(attrs={'placeholder': 'Year Established'}),
        }

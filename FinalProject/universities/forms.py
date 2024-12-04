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


class UniversitySelectionForm(forms.Form):
    existing_university = forms.ModelChoiceField(
        queryset=University.objects.all(),
        required=False,  # Optional field
        empty_label="-- Select an existing university --",
        label="Existing University",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    new_university_name = forms.CharField(
        max_length=150,
        required=False,  # Optional field
        label="New University Name",
        widget=forms.TextInput(attrs={'placeholder': 'Enter new university name if not listed', 'class': 'form-control'}),
    )
    country = forms.CharField(
        max_length=100,
        required=False,  # Only required if creating a new university
        label="Country",
        widget=forms.TextInput(attrs={'placeholder': 'Country', 'class': 'form-control'}),
    )
    city = forms.CharField(
        max_length=100,
        required=False,  # Only required if creating a new university
        label="City",
        widget=forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control'}),
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Short description of the university', 'class': 'form-control'}),
        label="Description",
    )
    year_established = forms.IntegerField(
        required=False,  # Optional field for the year established
        label="Year Established",
        widget=forms.NumberInput(attrs={'placeholder': 'Year Established', 'class': 'form-control'})
    )

    logo_url = forms.URLField(
        required=False,  # Optional field for the logo URL
        label="Logo URL",
        widget=forms.URLInput(attrs={'placeholder': 'Logo URL', 'class': 'form-control'})
    )


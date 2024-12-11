from django import forms
from FinalProject.students.models import Message, Student


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your message here...'})

        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'field_of_study', 'year_of_study', 'location', 'bio', 'photo']

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name...'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name...'}),
            'field_of_study': forms.TextInput(attrs={'placeholder': 'What are you currently studying...'}),
            'year_of_study': forms.NumberInput(attrs={'placeholder': 'Which year of university are you currently in...'}),
            'location': forms.TextInput(attrs={'placeholder': 'Where is your university located...'}),
            'bio': forms.TextInput(attrs={'placeholder': 'Give us some interesting facts about you...'}),
            'photo': forms.URLInput(attrs={'placeholder': 'Share a photo of you if you want...'}),

        }

    def clean_year_of_study(self):
        year_of_study = self.cleaned_data.get('year_of_study')
        if year_of_study is not None and year_of_study <= 0:
            raise forms.ValidationError("Year of study must be a positive number.")
        return year_of_study


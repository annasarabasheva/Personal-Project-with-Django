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
    year_of_study = forms.IntegerField(
        min_value=1,  # Enforces a minimum value
        error_messages={
            'min_value': "Year of study must be greater than or equal to 1.",
            'invalid': "Enter a valid year of study.",
        }
    )

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'field_of_study', 'year_of_study', 'location', 'bio', 'photo']

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name...'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name...'}),
            'field_of_study': forms.TextInput(attrs={'placeholder': 'What are you currently studying...'}),
            'year_of_study': forms.NumberInput(attrs={
                'placeholder': 'Which year of university are you currently in...',
            }),
            'location': forms.TextInput(attrs={'placeholder': 'Where is your university located...'}),
            'bio': forms.TextInput(attrs={'placeholder': 'Give us some interesting facts about you...'}),
            'photo': forms.URLInput(attrs={'placeholder': 'Share a photo of you if you want...'}),
        }


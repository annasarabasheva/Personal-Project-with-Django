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
        fields = '__all__'

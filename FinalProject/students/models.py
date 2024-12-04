from django.contrib.auth import get_user_model
from django.db import models

from FinalProject.accounts.models import Profile
from FinalProject.universities.models import University

UserModel = get_user_model()


class Student(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name="student",  # Allows reverse lookup: profile.student
        help_text="The profile associated with this student",
    )

    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name="students",
        null=True,
        blank=True,
    )

    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
    )

    field_of_study = models.CharField(
        max_length=150,
    )

    year_of_study = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Current year of study (e.g., 1, 2, 3, etc.)"
    )

    location = models.CharField(
        max_length=100,
        blank=True,
        help_text="City or region where the student is currently based",
    )

    # Profile description for the student
    bio = models.TextField(
        blank=True,
        help_text="A short bio or description of the student"
    )

    photo = models.URLField(
        blank=True,
        null=True,
        help_text="Profile photo of the student"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.university.name}"

    class Meta:
        ordering = ["first_name", "last_name"]


class Message(models.Model):
    sender = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='sent_messages')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.student.first_name} {self.student.last_name} at {self.timestamp}"
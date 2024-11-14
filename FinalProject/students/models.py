from django.db import models

from FinalProject.universities.models import University


class Student(models.Model):
    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name="students"
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

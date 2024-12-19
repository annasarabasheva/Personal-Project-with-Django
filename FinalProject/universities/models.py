from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class University(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
    )

    country = models.CharField(
        max_length=100,
    )

    city = models.CharField(
        max_length=100,
    )

    logo_url = models.URLField(
        blank=True,
        null=True,
        help_text="Link to the university's logo image"
    )

    year_established = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Year the university was established",
    )

    created_by = models.OneToOneField(
        UserModel,
        on_delete=models.SET_NULL,
        related_name="university",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

from django.db import models


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

    description = models.TextField(
        blank=True,
        help_text="Short description of the university",
    )

    def __str__(self):
        return f"{self.name}, {self.country}"

    class Meta:
        ordering = ["name"]

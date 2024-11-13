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

    def __str__(self):
        return f"{self.name}, {self.country}"

    class Meta:
        ordering = ["name"]

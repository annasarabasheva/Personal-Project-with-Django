from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile'
    )

    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)
    is_student = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name

    def save(self, *args, **kwargs):
        print(f"Saving Profile: {self.user.username}, is_student={self.is_student}")
        super().save(*args, **kwargs)



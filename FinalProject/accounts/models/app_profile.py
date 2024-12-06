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
        # This is a more defensive approach to avoid potential None errors
        return self.user.username if self.user and hasattr(self.user, 'username') else "Anonymous"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



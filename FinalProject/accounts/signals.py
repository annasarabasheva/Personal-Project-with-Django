from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from FinalProject.accounts.models import Profile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create the profile only if it doesn't already exist
        Profile.objects.get_or_create(user=instance)
    else:
        # Ensure existing profiles are not reset unnecessarily
        instance.profile.save()


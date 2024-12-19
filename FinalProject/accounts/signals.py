from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from FinalProject.accounts.models import Profile
from FinalProject.students.models import Student

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
    else:
        instance.profile.save()
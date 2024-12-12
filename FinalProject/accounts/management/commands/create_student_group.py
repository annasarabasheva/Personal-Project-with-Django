from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from FinalProject.students.models import Student
from FinalProject.universities.models import University
from FinalProject.forum.models import Category, Thread, Post


class Command(BaseCommand):
    help = "Creates or updates the 'Student Group' with permissions for Students, Universities, Categories, Threads, and Posts"

    def handle(self, *args, **kwargs):
        # Create the group
        student_group, created = Group.objects.get_or_create(name='Student Group')

        # Define permissions
        student_permissions = [
            Permission.objects.get(content_type=ContentType.objects.get_for_model(Student), codename='view_student'),
        ]

        university_permissions = [
            Permission.objects.get(content_type=ContentType.objects.get_for_model(University), codename='view_university'),
            Permission.objects.get(content_type=ContentType.objects.get_for_model(University), codename='add_university'),
        ]

        category_permissions = [
            Permission.objects.get(content_type=ContentType.objects.get_for_model(Category), codename='view_category'),
            Permission.objects.get(content_type=ContentType.objects.get_for_model(Category), codename='add_category'),
            Permission.objects.get(content_type=ContentType.objects.get_for_model(Category), codename='delete_category'),
        ]

        thread_permissions = [
            Permission.objects.get(content_type=ContentType.objects.get_for_model(Thread), codename='view_thread'),
            Permission.objects.get(content_type=ContentType.objects.get_for_model(Thread), codename='add_thread'),
            Permission.objects.get(content_type=ContentType.objects.get_for_model(Thread), codename='delete_thread'),
        ]

        post_permissions = [
            Permission.objects.get(content_type=ContentType.objects.get_for_model(Post), codename='view_post'),
            Permission.objects.get(content_type=ContentType.objects.get_for_model(Post), codename='add_post'),
            Permission.objects.get(content_type=ContentType.objects.get_for_model(Post), codename='delete_post'),
        ]

        # Combine all permissions
        all_permissions = (
            student_permissions +
            university_permissions +
            category_permissions +
            thread_permissions +
            post_permissions
        )

        # Assign permissions to the group
        student_group.permissions.set(all_permissions)
        student_group.save()

        if created:
            self.stdout.write(self.style.SUCCESS("Student Group created successfully with all permissions."))
        else:
            self.stdout.write(self.style.WARNING("Student Group updated with additional permissions."))

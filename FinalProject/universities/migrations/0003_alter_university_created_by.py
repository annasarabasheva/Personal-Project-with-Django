# Generated by Django 4.2.16 on 2024-12-06 15:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('universities', '0002_university_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='university',
            name='created_by',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='university', to=settings.AUTH_USER_MODEL),
        ),
    ]

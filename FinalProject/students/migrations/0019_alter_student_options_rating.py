# Generated by Django 4.2.16 on 2024-12-12 16:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('students', '0018_remove_student_average_rating_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={},
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveIntegerField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='students.student')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='given_ratings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('student', 'user')},
            },
        ),
    ]

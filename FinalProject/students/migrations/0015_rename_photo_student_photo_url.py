# Generated by Django 4.2.16 on 2024-12-11 23:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0014_alter_student_year_of_study'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='photo',
            new_name='photo_url',
        ),
    ]
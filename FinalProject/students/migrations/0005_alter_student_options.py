# Generated by Django 4.2.16 on 2024-11-14 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_alter_student_photo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['first_name', 'last_name']},
        ),
    ]
# Generated by Django 4.2.16 on 2024-12-12 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0019_alter_student_options_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='average_rating',
            field=models.FloatField(default=0.0),
        ),
    ]

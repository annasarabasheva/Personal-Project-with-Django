# Generated by Django 4.2.16 on 2024-12-11 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0013_alter_student_year_of_study'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='year_of_study',
            field=models.PositiveIntegerField(),
        ),
    ]
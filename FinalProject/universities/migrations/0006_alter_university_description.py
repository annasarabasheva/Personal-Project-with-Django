# Generated by Django 4.2.16 on 2024-12-19 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('universities', '0005_alter_university_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='university',
            name='description',
            field=models.TextField(blank=True, help_text='Short description of the university', max_length=20, null=True),
        ),
    ]

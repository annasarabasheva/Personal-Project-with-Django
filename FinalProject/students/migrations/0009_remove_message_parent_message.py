# Generated by Django 4.2.16 on 2024-12-06 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_message_parent_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='parent_message',
        ),
    ]

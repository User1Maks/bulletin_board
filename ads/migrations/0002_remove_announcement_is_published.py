# Generated by Django 5.1.4 on 2024-12-23 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announcement',
            name='is_published',
        ),
    ]
# Generated by Django 4.0 on 2023-01-21 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personnelPlanet', '0020_tasks_assignedtoid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='weekEnd',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='weekStart',
        ),
    ]

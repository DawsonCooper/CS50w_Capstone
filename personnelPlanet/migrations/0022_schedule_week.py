# Generated by Django 4.0 on 2023-01-25 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnelPlanet', '0021_remove_schedule_weekend_remove_schedule_weekstart'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='week',
            field=models.CharField(default='null', max_length=35),
        ),
    ]
# Generated by Django 4.1.2 on 2022-12-26 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personnelPlanet', '0010_alter_clock_clockin_alter_clock_clockout'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messages',
            old_name='toUser',
            new_name='comapny',
        ),
    ]

# Generated by Django 4.1.2 on 2022-12-25 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnelPlanet', '0007_memo_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clock',
            name='clockOut',
            field=models.DateField(),
        ),
    ]

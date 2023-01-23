# Generated by Django 4.1.2 on 2022-12-20 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnelPlanet', '0004_alter_availability_shift'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.IntegerField()),
                ('day', models.CharField(max_length=12)),
                ('clockIn', models.DateField(auto_now_add=True)),
                ('clockOut', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.IntegerField()),
                ('monday', models.CharField(default='off', max_length=15)),
                ('tuesday', models.CharField(default='off', max_length=15)),
                ('wednesday', models.CharField(default='off', max_length=15)),
                ('thursday', models.CharField(default='off', max_length=15)),
                ('friday', models.CharField(default='off', max_length=15)),
                ('saturday', models.CharField(default='off', max_length=15)),
                ('sunday', models.CharField(default='off', max_length=15)),
            ],
        ),
        migrations.DeleteModel(
            name='Shifts',
        ),
        migrations.AlterField(
            model_name='availability',
            name='day',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='user',
            name='hoursWorked',
            field=models.FloatField(default=0),
        ),
    ]

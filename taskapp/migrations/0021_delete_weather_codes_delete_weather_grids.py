# Generated by Django 4.1.3 on 2023-02-23 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taskapp', '0020_weather_codes_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='weather_codes',
        ),
        migrations.DeleteModel(
            name='weather_grids',
        ),
    ]
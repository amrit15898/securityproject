# Generated by Django 4.1.3 on 2023-02-23 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_fore', '0005_alter_weather_grids_forecast_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weather_grids',
            name='sect_id',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
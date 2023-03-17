# Generated by Django 4.1.3 on 2023-03-03 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_fore', '0017_weather_send_temp_packet_forecast_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grids',
            name='grid_id',
            field=models.CharField(max_length=4, unique=True),
        ),
        migrations.AlterField(
            model_name='weather_codes',
            name='code',
            field=models.CharField(max_length=2, unique=True),
        ),
        migrations.AlterField(
            model_name='weather_codes',
            name='forecast',
            field=models.CharField(max_length=300, unique=True),
        ),
    ]
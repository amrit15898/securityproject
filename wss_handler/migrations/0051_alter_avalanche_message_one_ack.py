# Generated by Django 4.1.3 on 2023-03-15 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wss_handler', '0050_alter_weather_forecast_message_day_2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avalanche_message_one',
            name='ack',
            field=models.BooleanField(default=False),
        ),
    ]
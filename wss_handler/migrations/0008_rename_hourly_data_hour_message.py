# Generated by Django 4.1.3 on 2023-01-06 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wss_handler', '0007_alter_hourly_data_options'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Hourly_Data',
            new_name='hour_message',
        ),
    ]
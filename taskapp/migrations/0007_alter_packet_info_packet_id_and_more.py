# Generated by Django 4.1.3 on 2023-01-16 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskapp', '0006_packet_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packet_info',
            name='packet_id',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='packet_info',
            name='packet_type',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
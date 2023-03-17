# Generated by Django 4.1.3 on 2023-01-10 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wss_handler', '0013_query_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query_message',
            name='data_date',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='query_message',
            name='start_time',
            field=models.CharField(max_length=4),
        ),
        migrations.AlterField(
            model_name='query_message',
            name='stop_time',
            field=models.CharField(max_length=4),
        ),
    ]

# Generated by Django 4.1.3 on 2023-02-22 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wss_handler', '0042_avalanche_code_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='avalanche_message_two',
            name='ack',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='avalanche_message_two',
            name='data',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='avalanche_message_two',
            name='message_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='avalanche_message_two',
            name='sequence_num',
            field=models.IntegerField(default=0),
        ),
    ]
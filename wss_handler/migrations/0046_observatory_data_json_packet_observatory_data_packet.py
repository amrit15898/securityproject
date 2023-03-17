# Generated by Django 4.1.3 on 2023-02-26 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wss_handler', '0045_observatory_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='observatory_data',
            name='json_packet',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='observatory_data',
            name='packet',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

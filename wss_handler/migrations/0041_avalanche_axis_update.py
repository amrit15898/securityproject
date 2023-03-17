# Generated by Django 4.1.3 on 2023-02-13 06:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wss_handler', '0040_remove_avalanche_message_one_axis_id1_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avalanche_axis_update',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_on', models.DateTimeField(auto_now=True)),
                ('json_data', models.JSONField()),
                ('sequence_num', models.IntegerField()),
                ('ack', models.BooleanField(blank=True, null=True)),
                ('packet', models.CharField(max_length=255)),
                ('grid_id', models.CharField(max_length=4)),
                ('action_code', models.CharField(max_length=2)),
                ('axis_id', models.CharField(max_length=3)),
                ('axis_name', models.CharField(max_length=100)),
                ('send_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

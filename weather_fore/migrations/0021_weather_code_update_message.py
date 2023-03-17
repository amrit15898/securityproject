# Generated by Django 4.1.3 on 2023-03-05 20:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('weather_fore', '0020_alter_weather_area_update_message_send_on'),
    ]

    operations = [
        migrations.CreateModel(
            name='weather_code_update_message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_on', models.DateTimeField(auto_now=True)),
                ('message_type', models.IntegerField(default=96)),
                ('packet', models.CharField(max_length=255)),
                ('data', models.JSONField()),
                ('sequence_num', models.IntegerField()),
                ('ack', models.BooleanField(blank=True, null=True)),
                ('action_code', models.CharField(max_length=2)),
                ('avalanche_code', models.CharField(max_length=2)),
                ('code_details', models.CharField(max_length=100)),
                ('send_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

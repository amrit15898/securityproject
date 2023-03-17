# Generated by Django 4.1.3 on 2023-02-27 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wss_handler', '0048_snow_profile_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='avalanche_occurrence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received_on', models.DateTimeField(auto_now_add=True)),
                ('packet', models.CharField(max_length=255)),
                ('json_packet', models.JSONField()),
                ('message_type', models.IntegerField(default=83)),
                ('state_code', models.CharField(max_length=1)),
                ('station_code', models.CharField(max_length=4)),
                ('site_latitude', models.CharField(max_length=6)),
                ('site_longitude', models.CharField(max_length=6)),
                ('occurrence_date', models.CharField(max_length=6)),
                ('occurrence_time', models.CharField(max_length=4)),
                ('register_unregister', models.CharField(max_length=1)),
                ('grid_map_reference', models.CharField(max_length=14)),
                ('slope_aspect', models.CharField(max_length=2)),
                ('fresh_snow_amount', models.CharField(max_length=3)),
                ('strom_snow', models.CharField(max_length=3)),
                ('standing_snow', models.CharField(max_length=3)),
                ('type_of_avalanche', models.CharField(max_length=1)),
                ('avalanche_length', models.CharField(max_length=3)),
                ('avalanche_breadth', models.CharField(max_length=3)),
                ('avalanche_height', models.CharField(max_length=3)),
                ('cause_of_occurrence', models.CharField(max_length=1)),
                ('avalanche_accident', models.CharField(max_length=1)),
                ('no_of_persons_involved', models.CharField(max_length=3)),
                ('no_of_persons_dead', models.CharField(max_length=3)),
                ('avalanche_warning', models.CharField(max_length=1)),
                ('damage', models.CharField(max_length=60)),
            ],
        ),
    ]

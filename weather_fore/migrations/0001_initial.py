# Generated by Django 4.1.3 on 2023-02-23 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='weather_codes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('forecast', models.CharField(max_length=300)),
                ('code', models.CharField(max_length=50)),
                ('relation_in_char', models.CharField(max_length=255)),
                ('intensity', models.CharField(max_length=255)),
                ('area', models.CharField(max_length=255)),
                ('Legend', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='weather_grids',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('sect_id', models.FloatField()),
                ('forecast_area', models.CharField(max_length=50)),
                ('natsat_grids', models.CharField(max_length=1500)),
            ],
        ),
    ]
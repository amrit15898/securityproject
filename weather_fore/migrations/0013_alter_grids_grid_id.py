# Generated by Django 4.1.3 on 2023-02-27 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_fore', '0012_alter_grids_grid_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grids',
            name='grid_id',
            field=models.CharField(max_length=2550000, unique=True),
        ),
    ]

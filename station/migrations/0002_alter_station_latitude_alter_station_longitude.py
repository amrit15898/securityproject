# Generated by Django 4.1.3 on 2023-02-28 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('station', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='latitude',
            field=models.CharField(max_length=14),
        ),
        migrations.AlterField(
            model_name='station',
            name='longitude',
            field=models.CharField(max_length=14),
        ),
    ]
# Generated by Django 4.1.3 on 2023-03-03 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('station', '0005_alter_station_station_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('equation', models.TextField()),
            ],
        ),
    ]

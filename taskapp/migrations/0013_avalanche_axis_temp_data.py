# Generated by Django 4.1.3 on 2023-02-16 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskapp', '0012_avalanche_message_logs'),
    ]

    operations = [
        migrations.CreateModel(
            name='avalanche_axis_temp_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
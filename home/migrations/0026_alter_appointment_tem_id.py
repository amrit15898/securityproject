# Generated by Django 4.1.2 on 2022-12-04 05:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_appointment_reason_cancelation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='tem_id',
            field=models.UUIDField(default=uuid.UUID('0a59df87-da13-4b47-b7c9-917849ea8d5f')),
        ),
    ]

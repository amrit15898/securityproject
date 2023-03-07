# Generated by Django 4.1.7 on 2023-03-07 04:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0076_lab_alter_appointment_tem_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='visited',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='tem_id',
            field=models.UUIDField(default=uuid.UUID('1c5ce315-6739-4959-9182-bc1a6c123d22')),
        ),
    ]

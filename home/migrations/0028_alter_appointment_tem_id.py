# Generated by Django 4.1.2 on 2022-12-05 03:48

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_alter_appointment_tem_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='tem_id',
            field=models.UUIDField(default=uuid.UUID('4c00a469-b571-4345-ac83-e45669a2c6a1')),
        ),
    ]

# Generated by Django 4.1.7 on 2023-03-03 05:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0066_alter_appointment_tem_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='tem_id',
            field=models.UUIDField(default=uuid.UUID('93b202fb-87df-4628-a51e-a05ae6710d14')),
        ),
    ]

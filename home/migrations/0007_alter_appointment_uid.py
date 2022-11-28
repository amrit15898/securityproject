# Generated by Django 4.1.3 on 2022-11-23 21:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_appointment_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
# Generated by Django 4.1.7 on 2023-02-24 12:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0044_alter_appointment_tem_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='tem_id',
            field=models.UUIDField(default=uuid.UUID('5163dccf-c77d-498d-8142-015e14a423d9')),
        ),
        migrations.DeleteModel(
            name='pvt_employee',
        ),
    ]

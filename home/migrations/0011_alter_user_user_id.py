# Generated by Django 4.1.2 on 2022-11-26 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_remove_user_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]

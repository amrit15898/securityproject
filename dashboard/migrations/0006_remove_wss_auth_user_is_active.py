# Generated by Django 4.1.3 on 2023-02-13 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_alter_wss_auth_user_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wss_auth_user',
            name='is_active',
        ),
    ]

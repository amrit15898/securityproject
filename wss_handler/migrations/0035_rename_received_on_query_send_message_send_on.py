# Generated by Django 4.1.3 on 2023-01-30 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wss_handler', '0034_rename_received_on_reboot_message_send_on_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='query_send_message',
            old_name='received_on',
            new_name='send_on',
        ),
    ]

# Generated by Django 4.1.3 on 2023-01-24 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wss_handler', '0026_message_backup'),
    ]

    operations = [
        migrations.CreateModel(
            name='command_message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received_on', models.DateTimeField(auto_now=True)),
                ('current_date', models.CharField(max_length=6)),
                ('current_time', models.CharField(max_length=4)),
                ('terminal_id', models.CharField(max_length=5)),
                ('command_code', models.CharField(max_length=2)),
                ('query_message', models.CharField(max_length=12)),
                ('data', models.CharField(max_length=117)),
                ('send_data', models.JSONField(blank=True, null=True)),
                ('sequence_num', models.IntegerField()),
                ('ack', models.BooleanField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='reboot_message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received_on', models.DateTimeField(auto_now=True)),
                ('current_date', models.CharField(max_length=6)),
                ('current_time', models.CharField(max_length=4)),
                ('terminal_id', models.CharField(max_length=5)),
                ('reboot_code', models.CharField(max_length=2)),
                ('packet', models.JSONField(blank=True, null=True)),
                ('sequence_num', models.IntegerField()),
                ('ack', models.BooleanField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='message_backup',
            name='date',
            field=models.DateField(),
        ),
    ]
# Generated by Django 4.1.3 on 2022-11-23 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_appointment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='user',
        ),
        migrations.AddField(
            model_name='appointment',
            name='gh_dh',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gh_dh', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointment',
            name='tech_dir',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tech_dir', to=settings.AUTH_USER_MODEL),
        ),
    ]

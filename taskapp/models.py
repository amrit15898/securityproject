from django.db import models
from django.contrib.auth.models import User
try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField

# Create your models here.


class message_type(models.Model):
    key = models.IntegerField(unique=True)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value


class aws_query(models.Model):
    code = models.CharField(max_length=5, unique=True)
    title = models.CharField(max_length=255)


class Packet_Info(models.Model):
    packet_id = models.IntegerField(unique=True)
    packet_type = models.CharField(max_length=255, unique=True)


class weather_forecast_code(models.Model):
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=255)


class avalanche_grid(models.Model):
    grid_id = models.CharField(max_length=4, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)


class avalanche_axis(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    avalanche_axis = models.CharField(max_length=255)
    avalanche_axis_code = models.CharField(max_length=5, unique=True)  # avalanche_axis_id
    aor = models.CharField(max_length=255)
    grids = models.CharField(max_length=1000, null=True, blank=True)
    axis_code_afg = models.CharField(max_length=50, unique=True)


class avalanche_message_logs(models.Model):
    logs_on = models.DateTimeField(auto_now_add=True)
    message = models.TextField()


class avalanche_axis_temporary_data(models.Model):
    date = models.CharField(max_length=20)
    grid_id = models.CharField(max_length=1000)
    no_of_axis = models.IntegerField()
    avalanche_axis = JSONField(null=True, blank=True)
    avalanche_code = JSONField(null=True, blank=True)
    outlook = models.CharField(max_length=125, null=True, blank=True)





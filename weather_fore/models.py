from django.db import models
from django.contrib.auth.models import User
try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField
# Create your models here.


class Grids(models.Model):
    grid_id = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return self.grid_id


class weather_grids(models.Model):
    added_on = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, unique=True)
    sect_id = models.CharField(max_length=50, unique=True)
    forecast_area = models.CharField(max_length=50, unique=True)
    natsat_grids = models.ManyToManyField(Grids)


    def __str__(self):
        return self.name

class weather_codes(models.Model):
    added_on = models.DateTimeField(auto_now_add=True)
    forecast = models.CharField(max_length=300, unique=True)
    code = models.CharField(max_length=2, unique=True)
    relation_in_char = models.CharField(max_length=255, unique=True)
    intensity = models.CharField(max_length=255)
    area = models.CharField(max_length=255, null=True, blank=True)
    legend = models.CharField(max_length=255)


class weather_forecast_logs(models.Model):
    message = models.TextField()





class weather_send_temp_packet(models.Model):
    start_date = models.CharField(max_length=6)
    grid_id = models.CharField(max_length=4)
    num_of_day = models.CharField(max_length=2, default=1)
    forecast_area = models.CharField(max_length=3, null=True, blank=True)
    day_1 = models.CharField(max_length=2)
    day_2 = models.CharField(max_length=2, null=True, blank=True)
    day_3 = models.CharField(max_length=2, null=True, blank=True)
    day_4 = models.CharField(max_length=2, null=True, blank=True)
    day_5 = models.CharField(max_length=2, null=True, blank=True)
    day_6 = models.CharField(max_length=2, null=True, blank=True)




class weather_area_update_message(models.Model):
    send_on = models.DateTimeField(auto_now=True)
    send_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    message_type = models.IntegerField(default=96)
    packet = models.CharField(max_length=255)
    data = JSONField()
    sequence_num = models.IntegerField()
    ack = models.BooleanField(null=True, blank=True)
    grid_id = models.CharField(max_length=4)
    action_code = models.CharField(max_length=2)
    area_id = models.CharField(max_length=3)
    area_name = models.CharField(max_length=100)



class weather_code_update_message(models.Model):
    send_on = models.DateTimeField(auto_now=True)
    send_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    message_type = models.IntegerField(default=97)
    packet = models.CharField(max_length=255)
    data = models.JSONField()
    sequence_num = models.IntegerField()
    ack = models.BooleanField(null=True, blank=True)
    action_code = models.CharField(max_length=2)
    avalanche_code = models.CharField(max_length=2)
    code_details = models.CharField(max_length=100)


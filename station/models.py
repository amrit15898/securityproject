from django.db import models

# Create your models here.


class Station(models.Model):
    added_on = models.DateTimeField(auto_now_add=True)
    station_name = models.CharField(max_length=255)
    station_id = models.IntegerField(unique=True)
    latitude = models.CharField(max_length=14)
    longitude = models.CharField(max_length=14)
    terminal_id = models.IntegerField()

class Sensors(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    sensor_id = models.CharField(max_length=3)
    sensor_name = models.CharField(max_length=255, null=True, blank=True)
    unit = models.CharField(max_length=255, null=True, blank=True)
    equation = models.CharField(max_length=255, null=True, blank=True)



class Equation(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    equation = models.TextField()


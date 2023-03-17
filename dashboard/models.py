from django.db import models
from django.contrib.auth.models import User
# Create your models here.



POINT_CHOICES = (
    ("marker", "marker"),
    ("label", "label"),
    ("station","station")
)


class Pointers(models.Model):
    title = models.CharField(max_length=255)
    longitude = models.FloatField()
    latitude = models.FloatField()
    point_type = models.CharField(max_length=255, choices=POINT_CHOICES)
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "pointer"
        unique_together = ('longitude', 'latitude',)



class wss_auth_user(models.Model):
    create_on = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.username


class user_activity(models.Model):
    on_activity = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    task_details = models.TextField()


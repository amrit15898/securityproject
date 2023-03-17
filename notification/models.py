from django.db import models

# Create your models here.
class Notifications(models.Model):
    notification_on = models.DateTimeField(auto_now_add=True)
    noti_for = models.CharField(max_length=255,)
    message = models.CharField(max_length=255)
    status = models.BooleanField(default=False)


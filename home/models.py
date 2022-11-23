from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .manager import *

# Create your models here.
postions = (("Director", "Director"),
("Associate Director","Associate Director"),
("Tech Director","Tech Director"),
("GH/DH ","GH/DH "),
("Employee", "Employee"))
class Department(models.Model):
    name = models.CharField(max_length=50)

class User(AbstractBaseUser, PermissionsMixin):
    department = models.ForeignKey(Department, on_delete= models.CASCADE, null=True, blank=True)
    position = models.CharField(max_length = 40, choices=postions)
    name = models.CharField(max_length=150, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)
    objects = UserManager()
    USERNAME_FIELD = 'name'
    # REQUIRED_FIELDS = ['department', 'position']
status = (("Approved", "Approved"),("Not Approved", "Not Approved"), ("Pending", "Pending"))
class Appointment(models.Model):
    r_user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="r_user")
    user = models.ForeignKey(User, on_delete= models.CASCADE,related_name="user")
    date = models.DateTimeField(auto_now_add=False)
    description = models.TextField()
    department = models.ForeignKey(Department ,on_delete=models.CASCADE)
    dh_gh_clr = models.CharField(max_length=50, choices=status , null=True, blank=True, default="Pending")
    tech_dir_clr = models.CharField(max_length=50, choices=status , null=True, blank=True, default="Pending")
    ass_dir_clr = models.CharField(max_length=50, choices=status , null=True, blank=True, default="Pending")
    dir_clr = models.CharField(max_length=50, choices=status , null=True, blank=True, default="Pending")





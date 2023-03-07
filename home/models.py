from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .manager import *
import uuid
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
# Create your models here.
postions = (("Director", "Director"),
("Associate Director","Associate Director"),
("Tech Director","Tech Director"),
("GH/DH","GH/DH"),
("Employee", "Employee"),
("Security officer", "Security officer"),
("oic", "oic"),
("hwmg", "hwmg"))


class Department(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.name

class User(AbstractBaseUser, PermissionsMixin):
    position = models.CharField(max_length = 40, choices=postions)
    name = models.CharField(max_length=150)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="images", null=True, blank=True)
    employee_id = models.CharField(max_length=20, null=True, blank=True, unique = True)   
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    adhaar_no = models.CharField(max_length=20, null=True, blank=True, default=None)
    location = models.TextField(null=True, blank=True, default=None)
    department_access = models.BooleanField(default=False, null=True, blank=True)
    pis = models.CharField(max_length=200, unique=True)
    so_ld = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'pis'
    
    def __str__(self) -> str:
        return self.name
    # REQUIRED_FIELDS = ['department', 'position']
status = (("Approved", "Approved"),("Not Approved", "Not Approved"), ("Pending", "Pending"))
clearance_level = (("red", "red"), ("green", "green"), ("yellow", "yellow"), ("brown", "brown"))
visit_domain = (("visited", "visited"), ("not visited", "not visited"), ("pending", "pending"))
class Appointment(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True, related_name="postted_byy")
    pvt_request = models.BooleanField(default=False)
    name = models.CharField(max_length=200 , null=True,blank=True)
    age = models.CharField(max_length=20 , null=True,blank=True)
    height = models.CharField(max_length=20 , null=True,blank=True)
    organization_name = models.CharField(max_length=200, null=True, blank=True)
    r_user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="r_user")
    gh_dh = models.ForeignKey(User, on_delete= models.CASCADE,related_name="gh_dh", null=True, blank=True)
    tech_dir = models.ForeignKey(User, on_delete= models.CASCADE,related_name="tech_dir", null=True, blank=True)
    clearance_level = models.CharField(max_length= 200, choices=clearance_level)
    accommodation_requirement= models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=False)
    transporation_requirement = models.BooleanField(default=False)
    description = models.TextField()
    # department = models.ForeignKey(Department ,on_delete=models.CASCADE)
    dh_gh_clr = models.CharField(max_length=50, choices=status , null=True, blank=True, default="Pending")
    tech_dir_clr = models.CharField(max_length=50, choices=status , null=True, blank=True, default="Pending")
    ass_dir_clr = models.CharField(max_length=50, choices=status , null=True, blank=True, default="Pending")
    dir_clr = models.CharField(max_length=50, choices=status , null=True, blank=True, default="Pending")
    send_security = models.BooleanField(default=False, null=True, blank=True)
    ld = models.ForeignKey(User, on_delete=models.CASCADE , null=True, blank=True)
    tem_id = models.UUIDField(default=uuid.uuid4())
    reason_cancelation = models.TextField(null = True, blank=True)   
    items = models.TextField(null=True, blank=True, default=None)  
    purpose = models.TextField(null=True, blank=True, default=None)
    duration = models.CharField(max_length=20, null=True, blank=True)
    final_clearance = models.BooleanField(default=False)
    send_oic = models.BooleanField(default=False)
    perm_id = models.UUIDField(null=True, blank=True)
    close_clearance = models.BooleanField(default=False)
    close_clearance_reason = models.TextField(null=True, blank=True)
    visited_staus = models.CharField(max_length=200, choices= visit_domain ,default="pending")

@receiver(pre_save, sender=Appointment)
def create_perm_id(sender, instance, **kwargs):
    # TaskDate.objects.create(task = instance, date = datetime.now())
    if instance.final_clearance == True:
        print("yess is called")
        uid = uuid.uuid4()
        instance.perm_id = uid
        
class Clearance(models.Model):
    type = models.CharField(max_length=200, null=True ,blank=True)
    
class ForgetMessageRequest(models.Model):
    employee_id = models.ForeignKey(User, on_delete=models.CASCADE)

class DownloadFile(models.Model):
    d_file = models.FileField(upload_to="download_files")
    

class Lab(models.Model):
    name = models.CharField(max_length=200)

    


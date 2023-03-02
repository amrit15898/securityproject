from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(User)
class user_admin_register(admin.ModelAdmin):
    list_display = ["name", "position"]
    
    
admin.site.register(Department)
@admin.register(Appointment)
class Appointment_Register(admin.ModelAdmin):
    list_display = ["r_user", "description", "date"]

admin.site.register(DownloadFile)

admin.site.register(Clearance)
admin.site.register(ForgetMessageRequest)

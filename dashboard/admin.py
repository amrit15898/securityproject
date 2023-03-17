from django.contrib import admin
from .models import *
# Register your models here.



admin.site.site_header = "DGRE"
admin.site.site_title = "DGRE "
admin.site.index_title = "DGRE"



class pointer(admin.ModelAdmin):
    list_display = ["title", "longitude", "latitude", "point_type", "create_at"]

admin.site.register(Pointers, pointer)
admin.site.register(wss_auth_user)

class activity(admin.ModelAdmin):
    list_display = ["id", "on_activity", "user", "task_details"]
admin.site.register(user_activity, activity)



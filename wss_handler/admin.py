from django.contrib import admin
from .models import ws_sessions, Receive_message, Websocket_Status, Query_Send_Message, message_backup, \
    command_message, reboot_message, site_critical_alert, Avalanche_message_one, Avalanche_message_two, \
    observatory_data, snow_profile_data, snow_strom_data, Weather_Forecast_Message, Avalanche_axis_update, \
    Avalanche_code_update


# Register your models here.




class receiver_sms(admin.ModelAdmin):
    list_display = ["id", "received_on", "packet_data", "data"]

admin.site.register(Receive_message, receiver_sms)
admin.site.register(ws_sessions)


class running_detail(admin.ModelAdmin):
    list_display = ["id", "started_at", "closed_at", "is_run"]

admin.site.register(Websocket_Status, running_detail)

class query_message(admin.ModelAdmin):
    list_display = ['id', "data", "send_by", "ack"]
admin.site.register(Query_Send_Message, query_message)
admin.site.register(message_backup)
admin.site.register(command_message)
admin.site.register(reboot_message)
admin.site.register(site_critical_alert)
admin.site.register(Avalanche_message_one)
admin.site.register(Avalanche_message_two)
admin.site.register(observatory_data)
admin.site.register(snow_profile_data)
admin.site.register(snow_strom_data)
admin.site.register(Weather_Forecast_Message)
admin.site.register(Avalanche_axis_update)
admin.site.register(Avalanche_code_update)




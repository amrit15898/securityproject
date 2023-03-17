from django.contrib import admin
from .models import message_type, aws_query, Packet_Info, weather_forecast_code, avalanche_grid, avalanche_axis,\
    avalanche_message_logs, avalanche_axis_temporary_data
# Register your models here.




class Message_type(admin.ModelAdmin):
    list_display = ["key", "value"]

admin.site.register(message_type, Message_type)



class aws(admin.ModelAdmin):
    list_display = ["code", "title"]

admin.site.register(aws_query, aws)


class packet(admin.ModelAdmin):
    list_display = ["packet_id", "packet_type"]

admin.site.register(Packet_Info, packet)

class weather_forecast(admin.ModelAdmin):
    list_display = ["code", "title"]

admin.site.register(weather_forecast_code, weather_forecast)

class avalanche_grids(admin.ModelAdmin):
    list_display = ["grid_id", "created_on"]

admin.site.register(avalanche_grid, avalanche_grids)

class Avalanche_axis_db(admin.ModelAdmin):
    list_display = ["avalanche_axis", "avalanche_axis_code", "aor", "grids", "axis_code_afg"]
admin.site.register(avalanche_axis, Avalanche_axis_db)

admin.site.register(avalanche_message_logs)
admin.site.register(avalanche_axis_temporary_data)

from django.contrib import admin
from .models import *

# Register your models here.



class weather_grid(admin.ModelAdmin):
    list_display = ["name", "sect_id", "forecast_area", "added_on"]

admin.site.register(weather_grids, weather_grid)

class WeatherCode(admin.ModelAdmin):
    list_display = ["forecast", "code", 'relation_in_char', "intensity", "area", "legend"]

admin.site.register(weather_codes, WeatherCode)
admin.site.register(weather_forecast_logs)
admin.site.register(Grids)
admin.site.register(weather_send_temp_packet)
admin.site.register(weather_area_update_message)
admin.site.register(weather_code_update_message)

from django.db import models
import random
try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
# Create your models here.



class ws_sessions(models.Model):
    connect_on = models.DateTimeField(auto_now=True)
    session_id = models.CharField(max_length=255)
    packet_id = models.CharField(max_length=100)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    logout_on = models.DateTimeField(null=True, blank=True)
    logout = models.BooleanField(default=False)
    log_message = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.session_id



class Receive_message(models.Model):
    received_on = models.DateTimeField(auto_now=True)
    data = models.CharField(max_length=255)
    message_type = models.CharField(max_length=2)
    aws_date = models.CharField(max_length=6)
    aws_time = models.CharField(max_length=4)
    station_id = models.CharField(max_length=5)
    sensor_code = models.CharField(max_length=2)
    packet_data = models.CharField(max_length=117)
    packet = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.message_type



class Running_details(models.Model):
    is_run = models.BooleanField(default=False)
    started_at = models.DateTimeField()
    closed_at = models.DateTimeField(null=True, blank=True)


class Websocket_Status(models.Model):
    is_run = models.BooleanField(default=False)
    started_at = models.DateTimeField()
    closed_at = models.DateTimeField(null=True, blank=True)



class Query_Send_Message(models.Model):
    send_on = models.DateTimeField(auto_now=True)
    data = models.CharField(max_length=117)
    terminal_id = models.CharField(max_length=5)
    query_code = models.CharField(max_length=2)
    message_date = models.CharField(max_length=6)
    end_time = models.CharField(max_length=4)
    current_date = models.CharField(max_length=6)
    current_time = models.CharField(max_length=4)
    sequence_num = models.IntegerField()
    send_data = JSONField(null=True, blank=True)
    ack = models.BooleanField(null=True, blank=True)
    send_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)





class message_backup(models.Model):
    create_on = models.DateTimeField(auto_now=True)
    date = models.DateField()
    file_path = models.CharField(max_length=255, null=True, blank=True)


class command_message(models.Model):
    received_on = models.DateTimeField(auto_now=True)
    current_date = models.CharField(max_length=6)
    current_time = models.CharField(max_length=4)
    terminal_id = models.CharField(max_length=5)
    command_code = models.CharField(max_length=2)
    query_message = models.CharField(max_length=12)
    data = models.CharField(max_length=117)
    json_data = JSONField(null=True, blank=True)
    sequence_num = models.IntegerField()
    ack = models.BooleanField(null=True, blank=True)
    send_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)


class reboot_message(models.Model):
    send_on = models.DateTimeField(auto_now=True)
    current_date = models.CharField(max_length=6)
    current_time = models.CharField(max_length=4)
    terminal_id = models.CharField(max_length=5)
    reboot_code = models.CharField(max_length=2)
    json_data = JSONField(null=True, blank=True)
    sequence_num = models.IntegerField()
    ack = models.BooleanField(null=True, blank=True)
    send_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)


class Weather_Forecast_Message(models.Model):
    send_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    send_on = models.DateTimeField(auto_now=True)
    json_data = JSONField(null=True, blank=True)
    sequence_num = models.IntegerField()
    ack = models.BooleanField(null=True, blank=True)
    start_date = models.CharField(max_length=6)
    grid_id = models.CharField(max_length=4)
    num_of_forecast_day = models.CharField(max_length=2)
    forecast_area = models.CharField(max_length=3)
    day_1 = models.CharField(max_length=2)
    day_2 = models.CharField(max_length=2, null=True, blank=True)
    day_3 = models.CharField(max_length=2, null=True, blank=True)
    day_4 = models.CharField(max_length=2, null=True, blank=True)
    day_5 = models.CharField(max_length=2, null=True, blank=True)
    day_6 = models.CharField(max_length=2, null=True, blank=True)
    packet = models.CharField(max_length=255, null=True, blank=True)


class site_critical_alert(models.Model):
    send_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    send_on = models.DateTimeField(auto_now=True)
    json_data = JSONField(null=True, blank=True)
    sequence_num = models.IntegerField()
    ack = models.BooleanField(null=True, blank=True)
    start_date = models.CharField(max_length=6)
    grid_id = models.CharField(max_length=4)
    packet = models.CharField(max_length=255)
    num_of_day = models.CharField(max_length=2)
    avalanche_axis_id = models.CharField(max_length=3)
    alert_message = models.TextField(max_length=100)


class Avalanche_message_one(models.Model):
    sender_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    file = models.FileField(upload_to="avalanche_files/", null=True, blank=True)
    ack = models.BooleanField(default=False)
    sequence_num = models.IntegerField()
    message_on = models.DateTimeField(auto_now_add=True)
    data = JSONField()
    packet = models.CharField(max_length=255)
    message_type = models.IntegerField(default=91)
    start_date = models.CharField(max_length=6)
    grid_id = models.CharField(max_length=4)
    num_of_axis = models.IntegerField(range(1, 16))
    axis_ids = models.CharField(max_length=1000, null=True, blank=True)
    forecast_codes = models.CharField(max_length=1000, null=True, blank=True)



class Avalanche_message_two(models.Model):
    avalanche_one = models.ForeignKey(Avalanche_message_one, on_delete=models.DO_NOTHING)
    message_type = models.IntegerField(default=98)
    forecast_start_date = models.CharField(max_length=6)
    grid_id = models.CharField(max_length=4)
    outlook = models.CharField(max_length=124)
    data = JSONField(null=True, blank=True)
    message_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)



class Avalanche_axis_update(models.Model):
    send_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    send_on = models.DateTimeField(auto_now=True)
    json_data = JSONField()
    sequence_num = models.IntegerField()
    ack = models.BooleanField(null=True, blank=True)
    packet = models.CharField(max_length=255)
    grid_id = models.CharField(max_length=4)
    action_code = models.CharField(max_length=2)
    axis_id = models.CharField(max_length=3)
    axis_name = models.CharField(max_length=100)



class Avalanche_code_update(models.Model):
    send_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    send_on = models.DateTimeField(auto_now=True)
    json_data = JSONField()
    sequence_num = models.IntegerField()
    ack = models.BooleanField(null=True, blank=True)
    packet = models.CharField(max_length=255)
    action_code = models.CharField(max_length=2)
    avalanche_code = models.CharField(max_length=3)
    code_details = models.CharField(max_length=100)


class observatory_data(models.Model):
    received_on = models.DateTimeField(auto_now_add=True)
    packet = models.CharField(max_length=255, null=True, blank=True)
    json_packet = models.JSONField(null=True, blank=True)
    message_type = models.IntegerField(default=80)
    state_code = models.IntegerField(range(1, 9))
    station_code = models.IntegerField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    date = models.DateField()
    time = models.TimeField()
    max_temperature = models.IntegerField()
    min_temperature = models.IntegerField()
    dry_bulb_temperature = models.IntegerField()
    wet_bulb_temperature = models.IntegerField()
    atmospheric_pressure = models.IntegerField()
    initial_anemometer_reading = models.CharField(max_length=255)
    wind_direction = models.CharField(max_length=255)
    speed_kmph = models.CharField(max_length=25)
    average_wind_speed = models.CharField(max_length=25)
    rh = models.CharField(max_length=25)
    cloud_amount = models.CharField(max_length=8)
    cloud_type = models.CharField(max_length=2)
    present_weather = models.CharField(max_length=2)
    fresh_snow_amount = models.CharField(max_length=3)
    fresh_snow_duration = models.CharField(max_length=4)
    fresh_snow_density = models.CharField(max_length=3)
    crystal_type_code = models.CharField(max_length=2)
    fresh_snow_water_equivalent = models.CharField(max_length=3)
    rainfall = models.CharField(max_length=4)
    total_snow_amount = models.CharField(max_length=3)
    total_snow_water_equivalent = models.CharField(max_length=3)
    standing_snow = models.CharField(max_length=4)
    snow_surface_temperature = models.CharField(max_length=3)
    snow_characteristic_code = models.CharField(max_length=2)
    snow_appearance_code = models.CharField(max_length=1)
    free_penetration = models.CharField(max_length=2)
    crust_thickness = models.CharField(max_length=2)
    penetration_below_crust = models.CharField(max_length=2)
    sunshine = models.CharField(max_length=4)
    avalanche_feedback = models.CharField(max_length=1)
    avalanche_warning = models.CharField(max_length=1)





class snow_strom_data(models.Model):
    received_on = models.DateTimeField(auto_now_add=True)
    packet = models.CharField(max_length=255)
    json_packet = models.JSONField()
    message_type = models.IntegerField(default=81)
    state_code = models.IntegerField(range(1, 9))
    station_code = models.IntegerField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    date = models.CharField(max_length=6)
    time_commencement = models.TimeField()
    strom = models.CharField(max_length=1)
    strom_number = models.IntegerField()
    time_of_observation = models.CharField(max_length=4)
    strom_status = models.CharField(max_length=1)
    present_weather = models.CharField(max_length=2)
    cloud_amount = models.CharField(max_length=1)
    cloud_type = models.CharField(max_length=2)
    rainfall = models.CharField(max_length=4)
    anemometer_reading = models.CharField(max_length=6)
    average_wind_speed = models.CharField(max_length=3)
    wind_direction = models.CharField(max_length=2)
    dry_bulb_temperature = models.CharField(max_length=3)
    wet_bulb_temperature = models.CharField(max_length=3)
    rh = models.CharField(max_length=2)
    fresh_snow_amount = models.CharField(max_length=3)
    fresh_snow_duration = models.CharField(max_length=4)
    total_fresh_snow_amount = models.CharField(max_length=3)
    standing_snow = models.CharField(max_length=3)
    snow_temperature = models.CharField(max_length=3)
    snow_characteristics_code = models.CharField(max_length=2)
    snow_appearance_code = models.CharField(max_length=1)
    snow_penetration = models.CharField(max_length=2)
    fresh_show_density = models.CharField(max_length=3)
    fresh_show_water_equivalent = models.CharField(max_length=3)
    crystal_type_code = models.CharField(max_length=2)
    storm_board_reading = models.CharField(max_length=3)
    hourly_board_reading_24 = models.CharField(max_length=3)




class snow_profile_data(models.Model):
    received_on = models.DateTimeField(auto_now_add=True)
    packet = models.CharField(max_length=255)
    json_packet = models.JSONField()
    message_type = models.IntegerField(default=82)
    state_code = models.IntegerField(range(1, 9))
    station_code = models.IntegerField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    date = models.CharField(max_length=6)
    time_start = models.TimeField()
    time_end = models.TimeField()
    slope_aspect = models.CharField(max_length=2)
    slope_angle = models.CharField(max_length=4)
    present_weather = models.CharField(max_length=2)
    cloud_amount = models.CharField(max_length=1)
    cloud_type = models.CharField(max_length=2)
    wind_dir = models.CharField(max_length=4)
    wind_speed = models.CharField(max_length=6)
    dry_bulb_temperature = models.CharField(max_length=3)
    wet_bulb_temperature = models.CharField(max_length=3)
    shear_frame_area = models.CharField(max_length=3)
    weight_of_tube_hammer = models.CharField(max_length=3)
    no_of_strokes = models.CharField(max_length=2)
    height_of_fail = models.CharField(max_length=3)
    total_penetration = models.CharField(max_length=2)
    penetration_n_strokes = models.CharField(max_length=3)
    nfh_p = models.CharField(max_length=3)
    ram_resistance = models.CharField(max_length=3)
    height_above_ground = models.CharField(max_length=3)
    snow_temperature = models.CharField(max_length=3)
    layer_no = models.CharField(max_length=2)
    layer_thickness = models.CharField(max_length=2)
    wetness = models.CharField(max_length=1)
    grain_type = models.CharField(max_length=2)
    grain_size = models.CharField(max_length=1)
    hardness = models.CharField(max_length=1)
    density = models.CharField(max_length=2)
    shear_strength = models.CharField(max_length=3)
    water_equivalent = models.CharField(max_length=3)



class avalanche_occurrence(models.Model):
    received_on = models.DateTimeField(auto_now_add=True)
    packet = models.CharField(max_length=255)
    json_packet = models.JSONField()
    message_type = models.IntegerField(default=83)
    state_code = models.CharField(max_length=1)
    station_code = models.CharField(max_length=4)
    site_latitude = models.CharField(max_length=6)
    site_longitude = models.CharField(max_length=6)
    occurrence_date = models.CharField(max_length=6)
    occurrence_time = models.CharField(max_length=4)
    register_unregister = models.CharField(max_length=1)
    grid_map_reference = models.CharField(max_length=14)
    slope_aspect = models.CharField(max_length=2)
    fresh_snow_amount = models.CharField(max_length=3)
    strom_snow = models.CharField(max_length=3)
    standing_snow = models.CharField(max_length=3)
    type_of_avalanche = models.CharField(max_length=1)
    avalanche_length = models.CharField(max_length=3)
    avalanche_breadth = models.CharField(max_length=3)
    avalanche_height = models.CharField(max_length=3)
    cause_of_occurrence = models.CharField(max_length=1)
    avalanche_accident = models.CharField(max_length=1)
    no_of_persons_involved = models.CharField(max_length=3)
    no_of_persons_dead = models.CharField(max_length=3)
    avalanche_warning = models.CharField(max_length=1)
    damage = models.CharField(max_length=60)



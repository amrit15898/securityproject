from django.urls import path, include
from . import views

urlpatterns = [
    path("add-station/", views.add_station),
    path("show-all/", views.view_all_station),
    path("sensor-equation/", views.station_sensor_equation),

]



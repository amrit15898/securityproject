from django.urls import path
from . import views

urlpatterns = [
    path('area-update/', views.weather_area_update),
    path('code-update/', views.weather_code_update),
    path('show-send-weather-messages/', views.show_send_weather),
    path("send-weather-forecast/", views.send_weather_forecast),
    path("add-grid/", views.add_grid),
    path("view-grids/", views.view_all_grids),
    path("add-code/", views.add_weather_code),
    path("view-code/", views.view_weather_code),
    path("add-grid-by-csv/", views.grid_add_by_csv),
    path('grid-csv-data/', views.grid_add_csv_reader),
    path('send-weather-csv/', views.weather_file_csv),
    path('send-read-csv/', views.weather_csv_read),
    path('grid-id-validate/', views.weather_grid_validate),
    path('grid-area-validate/', views.weather_area_validate),
    path('logs-messages/', views.weather_forecast_log),
    path("code-csv-upload/", views.upload_code_csv),
    path("code-csv-read/", views.code_csv_reader),
    path("view-area-update/", views.weather_area_update_view),
    path("view-code-update/", views.view_weather_code_update),



]



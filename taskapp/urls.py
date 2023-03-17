from django.urls import path, include, re_path
from .import views
from .services.csv_reader import csv_reader_kwargs
from .views import avalanche_kwargs

urlpatterns = [

    path("send-avalanche/", views.send_avalanche_forecast, name="message_sender", kwargs=avalanche_kwargs),
    path("hourly-data/", views.hourly_data_show),
    path("query-data/", views.data_query_show),
    path("health-query/", views.health_query_show),
    path("send-query/", views.send_query_message),
    path("data-logger/", views.data_logger),
    path("manual-data/", views.manual_data),
    path("health-query-code3/", views.health_query_code_three),
    path("show-send-query-message/", views.show_send_query_message),
    path("show-message-code-details/", views.message_type_info),
    path("show-aws-message-code-details/", views.aws_message_info),
    # path("send-command/", views.send_command_message),
    # path("send-reboot/", views.send_reboot_message),
    path("show-backups/", views.message_backup_info),
    path('send-critical-alert/', views.send_critical_alert),
    path('show-critical-alert/', views.show_critical_messages),
    path('avalanche-axis-update/', views.avalanche_axis_update),
    path('avalanche-code-update/', views.avalanche_code_update),
    path('show-avalanche-axis-update/', views.show_avalanche_axis_update),
    path('avalanche-upload-file/', views.Avalanche_file_send.as_view()),
    path('avalanche-csv-file/', views.avalanche_csv_file),
    path('avalanche-packet-sender/', views.avalanche_packet_sender),
    path('show-avalanche-messages/', views.show_avalanche_messages),
    path('show-avalanche-csv-logs-messages/', views.show_avalanche_csv_logs),
    path('show-avalanche-code-update/', views.show_avalanche_code_update),

]


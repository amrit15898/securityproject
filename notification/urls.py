from django.urls import path, include
from . import views

urlpatterns = [
    path("get/", views.view_notification),
    path("notification-counter/", views.notification_counter),
    path("notification-show/", views.view_all_notification),
    path("avalanche-grid-validate/", views.avalanche_grid_validator)
]



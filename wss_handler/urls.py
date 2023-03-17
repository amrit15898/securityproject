
from django.urls import path
from .import views



urlpatterns = [
    path("login/", views.wss_auth),
    path("dashboard/", views.ws_dashboard),
    path("connection/", views.ws_connect),
    path("history/", views.ws_connection_history),
    path("logout/", views.ws_logout),
    path("log-check/", views.socket_authentication),
    path("dash-logout/", views.wss_dashboard_logout),
    path("wss-log-change/", views.wss_login_success_create.as_view()),
    path("msg-ack/", views.message_ack.as_view()),


]


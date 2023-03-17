
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from core import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("dashboard.urls")),
    path("", include("chatapp.urls")),
    path("notification/", include("notification.urls")),
    path("message/", include("taskapp.urls")),
    path("wss/", include("wss_handler.urls")),
    path("weather/", include("weather_fore.urls")),
    path("station/", include("station.urls")),
    path("natsat-h/", include("natsat_h.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_URL)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

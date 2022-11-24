
from django.urls import path, include
from home.views import *

urlpatterns = [

    path("post-app", post_appointment, name="appointment"),
    path("show-request", show_request, name="showrequest"),


]

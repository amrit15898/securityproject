from django.urls import path
from .views import *

urlpatterns = [
   path("observatory-message/", show_observatory_message),

]


from django.urls import path, include
from .import consumer



ws_patterns = [
    path("socket-receive/<group_name>/", consumer.Message_receiver.as_asgi()),
    path("dgre-message-receiver/<group_name>/", consumer.Message_receiver.as_asgi()),

]


urlpatterns = [


]


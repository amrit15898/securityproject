# """
# ASGI config for core project.
#
# It exposes the ASGI callable as a module-level variable named ``application``.
#
# For more information on this file, see
# https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
# """
#
# import os
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
# from chatapp.urls import ws_patterns
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
#
# # application = get_asgi_application()
#
#
# application = ProtocolTypeRouter({
#     'http':get_asgi_application(),
#     "websocket": URLRouter(ws_patterns)
# })




import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django_asgi_app = get_asgi_application()

from django.conf import settings
from chatapp.urls import ws_patterns

# asgi_routes["http"] = django_asgi_app
# application = ProtocolTypeRouter(ws_patterns)

import os

from django.urls import re_path
from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from chatapp.middlewares import TokenAuthMiddleWare, TokenAuthMiddleware2
from channels.security.websocket import AllowedHostsOriginValidator

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    "websocket": URLRouter(ws_patterns)
})


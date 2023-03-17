from wss_handler.models import Websocket_Status
from django import template

register = template.Library()

@register.simple_tag
def ws_connection_check():
      data = Websocket_Status.objects.last()
      if data.is_run:
        return ""
      else:
          return "not connected"


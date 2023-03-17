from django.apps import AppConfig




# def startup():


class WssHandlerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wss_handler'

    def ready(self):
        from wss_handler.models import Websocket_Status, ws_sessions
        from datetime import datetime
        run_data = Websocket_Status.objects.last()
        run_data.is_run = False
        run_data.closed_at = datetime.now()
        run_data.save()
        ws_session = ws_sessions.objects.last()
        ws_session.logout_on = datetime.now()
        ws_session.logout = True
        ws_session.save()






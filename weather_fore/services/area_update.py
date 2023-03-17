from datetime import datetime
from weather_fore.models import weather_area_update_message
from wss_handler.models import ws_sessions
from chatapp.views import send_message_to_natsat
from asgiref.sync import async_to_sync
from wss_handler.services.message_sender import natsat_connector_message_sender

def weather_area_update_sequence():
    today_date = datetime.now().date()
    query = weather_area_update_message.objects.filter(send_on__date=today_date)
    if query.exists():
        last_seq = query.last()
        return last_seq.sequence_num + 1
    else:
        return 100






def area_update(
        user,
        grid_id,
        action_code,
        area_id,
        area_name
):
    message_type = 96

    packet = f"#@{message_type}{grid_id}{action_code}{area_id}{area_name}@#"
    session_data = ws_sessions.objects.last()
    sequence_number = weather_area_update_sequence()
    message_json = {
        "msg_type": message_type,
        "sender": session_data.username,
        "string_data": packet,
        "session_id": session_data.session_id,
        "sequence_number": sequence_number,
        "packet": 7,
        "grid_id": grid_id,
        "name": "weather area update",
        "content": packet
    }
    try:
        # send
        natsat_connector_message_sender(message_json)
        weather_area_update_message.objects.create(
            send_by=user,
            packet=packet,
            data=message_json,
            sequence_num=sequence_number,
            grid_id=grid_id,
            action_code=action_code,
            area_id=area_id,
            area_name=area_name
        )

        return True
    except Exception as e:
        print(e)
        return False


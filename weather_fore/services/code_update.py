from datetime import datetime
from weather_fore.models import weather_code_update_message
from wss_handler.models import ws_sessions
from wss_handler.services.message_sender import natsat_connector_message_sender

def weather_code_update_sequence():
    today_date = datetime.now().date()
    query = weather_code_update_message.objects.filter(send_on__date=today_date)
    if query.exists():
        last_seq = query.last()
        return last_seq.sequence_num + 1
    else:
        return 100



def weather_code_updator(
        user,
        action_code,
        avalanche_code,
        code_details
):
    message_type = 97
    packet = f"#@{message_type}{action_code}{avalanche_code}{code_details}@#"
    session_data = ws_sessions.objects.last()
    sequence_number = weather_code_update_sequence()
    message_json = {
        "msg_type": message_type,
        "sender": session_data.username,
        "string_data": packet,
        "session_id": session_data.session_id,
        "sequence_number": sequence_number,
        "packet": 6,
        "name": "weather code update",
        "content": packet
    }

    try:
        # send
        natsat_connector_message_sender(message_json)
        weather_code_update_message.objects.create(
            send_by=user,
            packet=packet,
            data=message_json,
            sequence_num=sequence_number,
            action_code=action_code,
            avalanche_code=avalanche_code,
            code_details=code_details
        )

        return True
    except Exception as e:
        print(e, "here")
        return False




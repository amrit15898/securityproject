from wss_handler.models import Avalanche_code_update, ws_sessions
from datetime import datetime
from chatapp.views import send_message_to_natsat
from asgiref.sync import async_to_sync

from wss_handler.services.message_sender import natsat_connector_message_sender

def avalanche_code_sequence_generator():
    today_date = datetime.now().date()
    query = Avalanche_code_update.objects.filter(send_on__date=today_date)
    if query.exists():
        last_seq = query.last()
        return last_seq.sequence_num + 1
    else:
        return 100




def avalanche_code_updator(
        user,
        action_code,
        avalanche_code,
        code_detail
):

    message_type = 95
    packet = f"#@{message_type}{action_code}{avalanche_code}{code_detail}@#"
    session_data = ws_sessions.objects.last()
    sequence_num = avalanche_code_sequence_generator()

    message_json = {
        "msg_type": message_type,
        "sender": session_data.username,
        "string_data": packet,
        "session_id": session_data.session_id,
        "sequence_number": sequence_num,
        "packet": 5,
        "name": "dgre-a-code",
        "content": packet
    }

    try:
        natsat_connector_message_sender(
            message_json
        )

        Avalanche_code_update.objects.create(
            send_by=user,
            json_data=message_json,
            sequence_num=sequence_num,
            packet=packet,
            action_code=action_code,
            avalanche_code=avalanche_code,
            code_details=code_detail
        )
        return True
    except Exception as e:
        print(e)
        return False


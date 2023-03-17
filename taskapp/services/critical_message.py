from wss_handler.models import site_critical_alert, ws_sessions
from chatapp.views import send_message_to_natsat
from asgiref.sync import async_to_sync
from datetime import datetime


def critical_sequence_generator():
    today_date = datetime.now().date()
    query = site_critical_alert.objects.filter(send_on__date=today_date)
    if query.exists():
        last_seq = query.last()
        return last_seq.sequence_num + 1
    else:
        return 10



def critical_alert(
        sender,
        start_date,
        grid_id,
        num_of_day,
        avalanche_axis_id,
        alert_message,
):
    message_type = 93
    message_encode = f"#@{message_type}{start_date}{grid_id}{num_of_day}{avalanche_axis_id}{alert_message}@#"
    sequence_number = critical_sequence_generator()
    session_data = ws_sessions.objects.last()
    message_json = {
        "msg_type": message_type,
        "sender": session_data.username,
        "string_data": message_encode,
        "session_id": session_data.session_id,
        "sequence_number": sequence_number,
        "packet": 3
    }
    site_critical_alert.objects.create(
        send_by=sender,
        json_data=message_json,
        sequence_num=sequence_number,
        start_date=start_date,
        grid_id=grid_id,
        num_of_day=num_of_day,
        avalanche_axis_id=avalanche_axis_id,
        alert_message=alert_message,
        packet=message_encode
    )
    try:
        async_to_sync(send_message_to_natsat)(message_json)
    except Exception as e:
        print(e)

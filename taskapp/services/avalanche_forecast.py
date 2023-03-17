from wss_handler.models import Avalanche_message_one, ws_sessions, Avalanche_message_two
from datetime import datetime
from wss_handler.services.message_sender import natsat_connector_message_sender


def avalanche_sequence_generator():
    today_date = datetime.now().date()
    query = Avalanche_message_one.objects.filter(message_on__date=today_date)
    if query.exists():
        last_seq = query.last()
        return last_seq.sequence_num + 1
    else:
        return 100

def avalanche_sequence_generator_two():
    query = Avalanche_message_one.objects.all().last()
    if query.exists():
        return query.sequence_num
    else:
        return 100



def avalanche_forecaster_packet_one(
        start_date,
        grid_id,
        num_axis,
        axis_ids,
        forecast_codes,

):
    message_type = 91
    packet = f"#@{message_type}{start_date}{grid_id}{num_axis}"

    for i, j in zip(axis_ids, forecast_codes):
        packet = packet + str(i) + str(j)

    packet = packet + "@#"

    return packet

def avalanche_packet_sender_message_one(
        user,
        packet,
        start_date,
        grid_id,
        num_axis,
        axis_ids,
        forecast_code
):
    session_data = ws_sessions.objects.last()
    sequence_num = avalanche_sequence_generator()
    message_type = 91
    message_json = {
        "msg_type": 92,
        "sender": session_data.username,
        "string_data": packet,
        "session_id": session_data.session_id,
        "sequence_number": sequence_num,
        "packet": 5,
        "grid_id": grid_id,
        "name": "avalanche msg 1",
        "content": f"avalanche msg one from dgre {packet}"
    }

    try:
        natsat_connector_message_sender(
           j_data=message_json, user=session_data.username, pwd=session_data.password
        )

        message1 = Avalanche_message_one.objects.create(
            packet=packet,
            message_type=message_type,
            start_date=start_date,
            grid_id=grid_id,
            num_of_axis=num_axis,
            axis_ids=','.join(axis_ids),
            forecast_codes=','.join(forecast_code),
            sequence_num=sequence_num,
            data=message_json,
            sender_user=user
        )
        return message1

    except Exception as e:
        print(e)


def avalanche_forecaster_message_two(
        start_date,
        grid_id,
        outlook
):
    message_type = 98
    message_encode = f"#@{message_type}{start_date}{grid_id}{outlook}@#"
    return message_encode

def avalanche_message_two_sender(
        message1,
        packet,
        date,
        grid_id,
        outlook
):
    message_type = 98
    session_data = ws_sessions.objects.last()
    sequence_num = avalanche_sequence_generator_two()
    message_json = {
        "msg_type": message_type,
        "sender": session_data.username,
        "string_data": packet,
        "session_id": session_data.session_id,
        "sequence_number": sequence_num,
        "packet": 5,
        "grid_id": grid_id,
        "name": "avalanche msg 2",
        "content": f"avalanche from dgre {packet}"
    }

    try:
        natsat_connector_message_sender(
            j_data=message_json, user=session_data.username, pwd=session_data.password
        )

        Avalanche_message_two.objects.create(
            avalanche_one=message1,
            forecast_start_date=date,
            grid_id=grid_id,
            outlook=outlook,
            data=message_json,
            sequence_num=sequence_num,
        )
    except Exception as e:
        print(e)





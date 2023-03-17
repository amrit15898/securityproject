from wss_handler.models import Weather_Forecast_Message, ws_sessions
from datetime import datetime
from wss_handler.services.message_sender import natsat_connector_message_sender

def weather_sequence_generator():
    today_date = datetime.now().date()
    query = Weather_Forecast_Message.objects.filter(send_on__date=today_date)
    if query.exists():
        last_seq = query.last()
        return last_seq.sequence_num + 1

    else:
        return 100



def weather_forecast(
         sender,
         start_date,
         grid_id,
         num_of_forecast_day,
         forecast_area,
         day_1='',
         day_2='',
         day_3='',
         day_4='',
         day_5='',
         day_6=''
                ):

    message_encode = f"#@92{start_date}{grid_id}{num_of_forecast_day}{forecast_area}{day_1}{day_2}{day_3}{day_4}{day_5}{day_6}@#"
    sequence_number = weather_sequence_generator()
    session_data = ws_sessions.objects.last()
    message_json = {
        "msg_type": 92,
        "sender": session_data.username,
        "string_data": message_encode,
        "session_id": session_data.session_id,
        "sequence_number": sequence_number,
        "packet": 2,
        "grid_id": grid_id,
        "name": "weather forecast message",
        "content": message_encode
    }

    try:
        natsat_connector_message_sender(message_json)
        Weather_Forecast_Message.objects.create(
            send_by=sender,
            json_data=message_json,
            sequence_num=sequence_number,
            start_date=start_date,
            grid_id=grid_id,
            num_of_forecast_day=num_of_forecast_day,
            forecast_area=forecast_area,
            day_1=day_1,
            day_2=day_2,
            day_3=day_3,
            day_4=day_4,
            day_5=day_5,
            day_6=day_6,
            packet=message_encode
        )
        return True
    except Exception as e:
        print(e)
        return False





from celery import shared_task
from .models import Websocket_Status, ws_sessions, Receive_message, message_backup
from datetime import datetime
from websocket import create_connection
import json
from .models import Receive_message
# from celery.task.control import revoke
from djqscsv import write_csv




@shared_task()
def data_backup():
    today_date = datetime.now().date()
    data = Receive_message.objects.filter(received_on__date=today_date).values(
        "message_type", "received_on", "data", "aws_date", "aws_time", "station_id",
        "sensor_code", "packet_data"
    )
    with open(f'media/backupdata/{today_date}.csv', 'wb') as csv_file:
        write_csv(data, csv_file)
        print(csv_file)
        message_backup.objects.create(
            file_path=csv_file.name,
            date=today_date
        )
    return "done"


@shared_task()
def message_ack():
    ws = create_connection("ws://127.0.0.1:9091/topic/public/notification/")
    while True:
        data = ws.recv()
        print(data)


from wss_handler.models import command_message
from datetime import datetime


def command_sequence_generator():
    today_date = datetime.now().date()
    query = command_message.objects.filter(received_on__date=today_date)
    if query.exists():
        last_seq = query.last()
        return last_seq.sequence_num + 1

    else:
        return 10

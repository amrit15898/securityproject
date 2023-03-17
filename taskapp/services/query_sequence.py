from wss_handler.models import Query_Send_Message
from datetime import datetime


def send_query_sequence_generator():
    today_date = datetime.now().date()
    query = Query_Send_Message.objects.filter(send_on__date=today_date)
    if query.exists():
        last_seq = query.last()
        return last_seq.sequence_num + 1

    else:
        return 10

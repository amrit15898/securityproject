from wss_handler.models import reboot_message
from datetime import datetime


def reboot_sequence_generator():
    today_date = datetime.now().date()
    query = reboot_message.objects.filter(send_on__date=today_date)
    if query.exists():
        last_seq = query.last()
        return last_seq.sequence_num + 1

    else:
        return 10

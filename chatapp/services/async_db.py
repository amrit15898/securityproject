from channels.db import database_sync_to_async
from chatapp.models import Message


async def connect(self):
    self.username = await self.get_name()


@database_sync_to_async
def Send_messages(self):
    data = Message.objects.filter(sms_type=False)
    print(data)
    return data





@database_sync_to_async
def Received_messages(self,data):

    print(data)




@database_sync_to_async
def All_messages(self):
    data = Message.objects.all()
    print(data)
    return data


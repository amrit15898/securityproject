from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from wss_handler.models import Receive_message
from notification.models import Notifications

# message receiver
class Message_receiver(AsyncConsumer):
    async def websocket_connect(self, event):
        group_name = self.scope['url_route']['kwargs']["group_name"]
        await self.channel_layer.group_add(group_name, self.channel_name)
        await self.send({
            "type": "websocket.accept",
        })

    async def websocket_receive(self, event):
        group_name = self.scope['url_route']['kwargs']["group_name"]
        # print(group_name)
        await self.send({
            "type": "websocket.send",
            "text": "done",
        })



        await self.channel_layer.group_send("notification_group", {
            "type": "message.notification",
            "message": event["text"]
        })



    async def message_notification(self, event):

        await self.send({
            "type": "websocket.send",
            "text": event["message"],
        })

    async def websocket_disconnect(self, event):
        group_name = self.scope['url_route']['kwargs']["group_name"]
        await self.channel_layer.group_discard(
            group_name,
            self.channel_name
        )
        raise StopConsumer()




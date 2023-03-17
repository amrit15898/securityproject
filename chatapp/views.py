import json
from django.shortcuts import render, redirect, HttpResponse
import random
import websockets
from channels.db import database_sync_to_async
from notification.models import Notifications
from wss_handler.models import ws_sessions, Query_Send_Message
from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer
kwargs_value = {"response": False, 'count': 0}

async def send_notification(message):
    async with websockets.connect("ws://127.0.0.1:8000/socket-receive/notification_group/") as websocket:
        await websocket.send(str(message))
        await websocket.recv()




async def send_message_query(message, user, sequence_number):
    async with websockets.connect("ws://127.0.0.1:8005/socket-send/group_name/") as websocket:
        session_data = await database_sync_to_async(ws_sessions.objects.last)()
        msg_json = {
            "msg_type": 60,
            "sender": session_data.username,
            "string_data": str(message),
            "session_id": session_data.session_id,
            "sequence_number": sequence_number,
            "packet": 8
        }
        query_message = await database_sync_to_async(Query_Send_Message.objects.last)()
        query_message.send_data = msg_json
        await database_sync_to_async(query_message.save)()
        await websocket.send(json.dumps(msg_json))
        await send_notification(f"message send to natsat {message}")
        data = await websocket.recv()

        noti = Notifications(
            noti_for="message send",
            message=f"send {message} by {user}"
        )
        print(data)
        await database_sync_to_async(noti.save)()
        return data




async def send_message_to_natsat(message):
    async with websockets.connect("ws://127.0.0.1:8005/socket-send/group_name/") as websocket:
        await websocket.send(json.dumps(message))
        await send_notification(f"message send to natsat {message}")
        data = await websocket.recv()
        print(data)













# @login_required(login_url='/login/')
# def Send_message(request, **kwargs):
#     success_message = False
#     if kwargs["count"] == 1:
#         kwargs_value["count"] = 0
#         success_message = True
#         kwargs_value["response"] = False
#
#     if request.method == "POST":
#         if request.FILES.get("message_file"):
#             excel_res = read_excel(request.FILES.get("message_file"))
#             print(excel_res)
#             if excel_res is False:
#                 not_valid = True
#                 return render(request, "message.html", locals())
#
#             message = json.loads(excel_res)
#             if request.POST["message"]:
#                 message["text"] = request.POST["message"]
#
#             asyncio.run(send_sms(message))
#
#             sms_instance = Message.objects.create(
#                 message_type=True,
#                 message_description=message,
#                 file=request.FILES["message_file"]
#             )
#
#         elif request.POST["message"]:
#             message = {
#                 "text": request.POST["message"]
#             }
#             asyncio.run(send_sms(message))
#
#             sms_instance = Message.objects.create(
#                 message_type=True,
#                 message_description=message,
#             )
#         kwargs_value["response"] = True
#         kwargs_value["count"] = 1
#         return redirect("/send-message/")
#         # return redirect(reverse("/send-message/response/",  kwargs={'kya': 'auth'}))
#     last_message = Message.objects.filter(message_type=True).last()
#     return render(request, "sockets/message.html", locals())








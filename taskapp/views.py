import time

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import message_type, aws_query, weather_forecast_code, avalanche_axis, avalanche_message_logs, avalanche_axis_temporary_data
from dashboard.services.admin_decorator import admin_required
from wss_handler.models import Receive_message, Query_Send_Message, command_message, reboot_message, ws_sessions, \
    message_backup, site_critical_alert, Websocket_Status, Avalanche_axis_update, Avalanche_message_one, \
    Avalanche_message_two, Avalanche_code_update
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import ast
from django.http import JsonResponse
from asgiref.sync import async_to_sync
from chatapp.views import send_message_query, send_message_to_natsat
from taskapp.services.query_sequence import send_query_sequence_generator
from taskapp.services.command_sequence import command_sequence_generator
from taskapp.services.reboot_sequence import reboot_sequence_generator
from taskapp.services.critical_message import critical_alert
from .services.avalanche_axis_update import avalanche_axis_updator
from .services.avalanche_code_update import avalanche_code_updator
from .services.avalanche_forecast import avalanche_forecaster_packet_one, avalanche_forecaster_message_two, \
    avalanche_packet_sender_message_one, avalanche_message_two_sender
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import AvalancheUpload
import pandas as pd
from django.contrib.auth.models import User
from django.core.cache import cache
from .services.csv_reader import csv_reader, csv_reader_kwargs


def wss_check():
    websock_status = Websocket_Status.objects.first()
    if websock_status.is_run is False:
        return False
    else:
        return True

avalanche_kwargs = {
    "send": False
}
@login_required(login_url='/login/')
def send_avalanche_forecast(request, **kwargs):

    if request.method == "POST":
        # message 1
        ws_status = Websocket_Status.objects.last()
        if ws_status.is_run is False:
            ws_not_connect = True
            message_types = message_type.objects.all()
            return render(request, "messages/send_avalanche.html", locals())
        message_code = 91
        start_date = request.POST['start_date']
        grid_id = request.POST['grid_id']
        num_axis = request.POST['num_axis']
        axis_ids = request.POST.getlist("avalanche-axis-id")
        forecast_codes = request.POST.getlist("forecast_codes")
        current_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        format_date = datetime.strftime(current_date, "%d%m%y")
        packet = avalanche_forecaster_packet_one(
            format_date,
            grid_id,
            num_axis,
            axis_ids,
            forecast_codes
        )

        message1 = avalanche_packet_sender_message_one(
            user=request.user,
            packet=packet,
            grid_id=grid_id,
            num_axis=num_axis,
            axis_ids=axis_ids,
            forecast_code=forecast_codes,
            start_date=format_date
        )
        # message 2
        message_code2 = 98
        outlook = request.POST['outlook']
        time.sleep(5)

        packet2 = avalanche_forecaster_message_two(
            start_date=format_date,
            grid_id=grid_id,
            outlook=outlook
        )

        avalanche_message_two_sender(
            message1=message1,
            packet=packet2,
            date=start_date,
            grid_id=grid_id,
            outlook=outlook
        )
        avalanche_kwargs['send'] = True
        return redirect("/message/send-avalanche/")

    if kwargs.get("send") is True:
        sent = True
        avalanche_kwargs['send'] = False

    message_types = message_type.objects.all()
    return render(request, "messages/send_avalanche.html", locals())




@login_required(login_url='/login/')
def hourly_data_show(request):
    today_date = datetime.now().date()
    search_data = {"message_type": "72"}
    if request.GET.get("search-date"):
        today_date = request.GET.get("search-date")
        search_data['received_on__date'] = today_date
    elif request.GET.get("search-data"):
        pass
    else:
        search_data['received_on__date'] = today_date
    messages = Receive_message.objects.filter(**search_data)
    return render(request, "messages/hourly-data.html", locals())





@login_required(login_url='/login/')
def data_query_show(request):
    today_date = datetime.now().date()
    search_data = {"message_type": "73"}
    if request.GET.get("search-date"):
        today_date = request.GET.get("search-date")
        search_data['received_on__date'] = today_date
    elif request.GET.get("search-data") is None:
        search_data['received_on__date'] = today_date
    messages = Receive_message.objects.filter(**search_data)

    return render(request, "messages/data-query.html", locals())



@login_required(login_url='/login/')
def health_query_show(request):
    today_date = datetime.now().date()
    search_data = {"message_type": "74"}
    if request.GET.get("search-date"):
        today_date = request.GET.get("search-date")
        search_data['received_on__date'] = today_date
    elif request.GET.get("search-data") is None:
        search_data['received_on__date'] = today_date
    messages = Receive_message.objects.filter(**search_data)
    return render(request, "messages/health-query.html", locals())



@login_required(login_url='/login/')
def data_logger(request):
    today_date = datetime.now().date()
    search_data = {"message_type": "70"}
    if request.GET.get("search-date"):
        today_date = request.GET.get("search-date")
        search_data['received_on__date'] = today_date
    elif request.GET.get("search-data") is None:
        search_data['received_on__date'] = today_date
    messages = Receive_message.objects.filter(**search_data)
    return render(request, "messages/data-logger.html", locals())

@login_required(login_url='/login/')
def manual_data(request):
    today_date = datetime.now().date()
    search_data = {"message_type": "71"}
    if request.GET.get("search-date"):
        today_date = request.GET.get("search-date")
        search_data['received_on__date'] = today_date
    elif request.GET.get("search-data") is None:
        search_data['received_on__date'] = today_date
    messages = Receive_message.objects.filter(**search_data)
    return render(request, "messages/mannul-data.html", locals())


@login_required(login_url='/login/')
def health_query_code_three(request):
    today_date = datetime.now().date()
    search_data = {"message_type": "75"}
    if request.GET.get("search-date"):
        today_date = request.GET.get("search-date")
        search_data['received_on__date'] = today_date
    elif request.GET.get("search-data") is None:
        search_data['received_on__date'] = today_date
    messages = Receive_message.objects.filter(**search_data)
    return render(request, "messages/health-query3.html", locals())





@login_required(login_url="/login/")
def send_query_message(request):
    aws_query_code = aws_query.objects.all()
    if request.method == "POST":
        query_code = request.POST['aws_query']
        terminal_id = request.POST['terminal_id']
        message_date = request.POST['message_date']
        end_time = request.POST['end_time']

        date = datetime.strptime(str(message_date), '%Y-%m-%d').date()
        m_date = datetime.strftime(date, "%d%m%y")
        time_temp = datetime.strptime(end_time, "%H:%M").time()
        e_time = time_temp.strftime("%H%M")
        current_data = datetime.now()
        current_date = datetime.strftime(current_data, "%d%m%y")
        current_time = datetime.strftime(current_data, "%H%M")
        try:
          message_code = message_type.objects.filter(value="query_message").last().key
        except Exception as e:
            print(e)
            message_code = 60
        message_encode = f"#@{message_code}{current_date}{current_time}{terminal_id}{query_code}{m_date}{e_time}@#"
        sequence_num = send_query_sequence_generator()

        db_data = Query_Send_Message.objects.create(
            data=message_encode,
            terminal_id=terminal_id,
            query_code=query_code,
            message_date=m_date,
            end_time=e_time,
            current_date=current_date,
            current_time=current_time,
            sequence_num=sequence_num,
            send_by=request.user
        )
        try:
          resp = async_to_sync(send_message_query)(message_encode, request.user.username, sequence_num)
        except Exception as e:
            print(e)

        return redirect("/message/send-query/")


    return render(request, "messages/send-query.html", locals())


@login_required(login_url="/login/")
def show_send_query_message(request):
    today_date = datetime.now().date()
    if request.GET.get("search-data"):
       messages = Query_Send_Message.objects.all()
       return render(request, "messages/show-send-query-message.html", locals())
    elif request.GET.get("search-date"):
        today_date = request.GET.get("search-date")
    messages = Query_Send_Message.objects.filter(send_on__date=today_date)
    return render(request, "messages/show-send-query-message.html", locals())


@login_required(login_url="/login/")
def message_type_info(request):
    messages = message_type.objects.all()
    return render(request, "messages/message-code-info.html", locals())


@login_required(login_url="/login/")
def aws_message_info(request):
    messages = aws_query.objects.all()
    return render(request, "messages/view-aws-code.html", locals())



@login_required(login_url="/login/")
def send_command_message(request):
    if request.method == "POST":
        mess_type = 61
        terminal_id = request.POST["terminal_id"]
        command_code = request.POST["command_code"]
        query_message = request.POST["query_message"]
        current_data = datetime.now()
        current_date = datetime.strftime(current_data, "%d%m%y")
        current_time = datetime.strftime(current_data, "%H%M")
        sequence_num = command_sequence_generator()
        string_message = f"#@{mess_type}{current_date}{current_time}{terminal_id}{command_code}{query_message}@#"
        session_data = ws_sessions.objects.last()
        if session_data.logout is False:
            json_message = {
                "msg_type": mess_type,
                "sender": session_data.username,
                "string_data": string_message,
                "session_id": session_data.session_id,
                "sequence_number": sequence_num,
                "packet": 25
            }
            cmd_message = command_message.objects.create(
                current_date=current_date,
                current_time=current_time,
                terminal_id=terminal_id,
                command_code=command_code,
                query_message=query_message,
                data=string_message,
                sequence_num=sequence_num,
                json_data=json_message,
                send_by=request.user
            )
            try:
              async_to_sync(send_message_to_natsat)(json_message)
            except Exception as e:
                print(e)
            return redirect("/message/send-command/")
        else:
            wss_fail = True
    return render(request, "messages/send-command.html", locals())



@login_required(login_url="/login/")
def send_reboot_message(request):
    if request.method == "POST":
        mess_type = 62
        terminal_id = request.POST['terminal_id']
        reboot_code = request.POST['reboot-code']
        current_data = datetime.now()
        current_date = datetime.strftime(current_data, "%d%m%y")
        current_time = datetime.strftime(current_data, "%H%M")
        string_message = f"#@{mess_type}{current_date}{current_time}{terminal_id}{reboot_code}@#"
        session_data = ws_sessions.objects.last()
        sequence_num = reboot_sequence_generator()
        if session_data.logout is False:
            json_message = {
                "msg_type": mess_type,
                "sender": session_data.username,
                "string_data": string_message,
                "session_id": session_data.session_id,
                "sequence_number": sequence_num,
                "packet": 25
            }
            reboot_message.objects.create(
                current_date=current_date,
                current_time=current_time,
                terminal_id=terminal_id,
                reboot_code=reboot_code,
                json_data=json_message,
                sequence_num=sequence_num,
                send_by=request.user
            )
            try:
              async_to_sync(send_message_to_natsat)(json_message)
            except Exception as e:
                print(e)
            return redirect("/message/send-reboot/")
        else:
            wss_fail = True

    return render(request, "messages/reboot-message.html", locals())



@login_required(login_url="/login/")
def message_backup_info(request):
    datas = message_backup.objects.all()[:50]
    if request.method == "POST":
        date = request.POST['search-date']
        datas = message_backup.objects.filter(date=date)
        messages = Receive_message.objects.filter(received_on__date=date)
    return render(request, "dashboard/message-backup.html", locals())


@login_required(login_url="/login/")
def send_critical_alert(request):
    if request.method == "POST":
        start_date = request.POST['start_date']
        grid_id = request.POST['grid_id']
        alert_valid = request.POST['alert_valid']
        avalanche_axis_id = request.POST['avalanche_axis_id']
        alert_message = request.POST['alert_message']
        current_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        format_date = datetime.strftime(current_date, "%d%m%y")
        critical_alert(request.user,
                       start_date=format_date,
                       grid_id=grid_id,
                       num_of_day=alert_valid,
                       avalanche_axis_id=avalanche_axis_id,
                       alert_message=alert_message,
                       )
    return render(request, "messages/send-critical-message.html", locals())


@login_required(login_url='/login/')
def show_critical_messages(request):
    date = datetime.now().date()
    if request.GET.get("search-data"):
        messages = site_critical_alert.objects.all()
        return render(request, "messages/show-critical-message.html", locals())
    elif request.GET.get("search-date"):
        date = request.GET.get("search-date")
    messages = site_critical_alert.objects.filter(send_on__date=date)
    return render(request, "messages/show-critical-message.html", locals())




axis_update_kwargs = {
    "send": False
}

@login_required(login_url="/login/")
def avalanche_axis_update(request):
    wss_status = wss_check()
    global axis_update_kwargs
    if request.method == "POST" and wss_status is True:
        grid_id = request.POST['grid_id']
        action_code = request.POST['action-code']
        axis_id = request.POST['axis-id']
        outlook = request.POST['outlook']
        message_status = avalanche_axis_updator(
            request.user,
            grid_id,
            action_code,
            axis_id,
            outlook
        )
        if message_status is True:
            axis_update_kwargs['send'] = True
            return redirect('/message/avalanche-axis-update/')
    try:
        if axis_update_kwargs['send'] is True:
            send = True
            axis_update_kwargs['send'] = False
    except Exception as e:
        print(e)
    return render(request, "messages/avalanche-axis-update.html", locals())


@login_required(login_url="/login/")
def show_avalanche_axis_update(request):
    today_date = datetime.now().date()
    if request.GET.get("search-data"):
        messages = Avalanche_axis_update.objects.all().order_by('-id')
        return render(request, "messages/show-avalanche-axis-update.html", locals())
    elif request.GET.get("search-date"):
        today_date = request.GET.get("search-date")

    messages = Avalanche_axis_update.objects.filter(send_on__date=today_date)
    return render(request, "messages/show-avalanche-axis-update.html", locals())



code_update_kwargs = {
    "send": False
}

@login_required(login_url="/login/")
def avalanche_code_update(request):
    global code_update_kwargs
    wss_status = wss_check()
    if request.method == "POST" and wss_status is True:
        action_code = request.POST['action-code']
        avalanche_code = request.POST['avalanche_code']
        outlook = request.POST['outlook']
        message_status = avalanche_code_updator(
            user=request.user,
            action_code=action_code,
            avalanche_code=avalanche_code,
            code_detail=outlook
        )
        code_update_kwargs['send'] = True
        if message_status is True:
            return redirect("/message/avalanche-code-update/")
    try:
        if code_update_kwargs['send'] is True:
            send = True
            code_update_kwargs['send'] = False
    except Exception as e:
        print(e)
    return render(request, "messages/avalanche-code-update.html", locals())



@login_required(login_url="/login/")
def show_avalanche_code_update(request):
    today_date = datetime.now().date()
    if request.GET.get("search-data"):
        messages = Avalanche_code_update.objects.all().order_by('-id')
        return render(request, "messages/show-avalanche-code-update.html", locals())
    elif request.GET.get("search-date"):
        today_date = request.GET.get("search-date")

    messages = Avalanche_code_update.objects.filter(send_on__date=today_date)
    return render(request, "messages/show-avalanche-code-update.html", locals())



class Avalanche_file_send(generics.RetrieveAPIView):
    serializer_class = AvalancheUpload
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        if cache.get("avalanche_csv"):
            data = csv_reader.read_my_csv(file=cache.get("avalanche_csv"))
            cache.delete("avalanche_csv")
            return Response(data)
        else:
            return Response({"details": "file not uploaded yet please upload file"})



@csrf_exempt
def avalanche_packet_sender(request):
    if request.method == "POST":
        if wss_check() is False:
            return JsonResponse("bad", safe=False, status=404)

        data = request.POST['packets']
        list_data = ast.literal_eval(data)
        response = []
        for i in list_data:
            grid_id = i['grid_id']
            num_axis = i["no_of_axis"]
            axis_ids = i["avalanche_axis"]
            avalanche_code = i["avalanche_code"]
            start_date = i['date']
            packet2 = i['packet2']
            outlook = i['outlook']
            packet = i['packet']

            message1 = avalanche_packet_sender_message_one(
                user=request.user,
                packet=packet,
                grid_id=grid_id,
                num_axis=num_axis,
                axis_ids=axis_ids,
                forecast_code=avalanche_code,
                start_date=start_date
            )
            avalanche_message_two_sender(
                message1=message1,
                packet=packet2,
                date=start_date,
                grid_id=grid_id,
                outlook=outlook
            )
            response.append({
                "id": i['id'],
                "status": True
            })
        for j in range(0, 455788):
            pass
        return JsonResponse(response, safe=False)




@login_required(login_url="/login/")
def avalanche_csv_file(request):
    file_upload = True

    if request.method == "POST":
        file = request.FILES['file']
        if file.content_type != 'text/csv':
            invalid = True
            return render(request, "messages/send_avalanche.html", locals())
        try:
          cache.delete("avalanche_csv")
        except Exception as e:
            print(e)
        cache.set("avalanche_csv", file, timeout=10000)
        cache.delete("log_messages")

        logs = avalanche_message_logs.objects.all()
        for i in logs:
            i.delete()

        return render(request, "messages/avalanche-csv-data.html", locals())
    message_types = message_type.objects.all()
    return render(request, "messages/send_avalanche.html", locals())



@login_required(login_url="/login/")
def show_avalanche_messages(request):
    today_date = datetime.now().date()
    if request.GET.get("search-date"):
        today_date = request.GET.get("search-date")
    elif request.GET.get("search-data"):
        messages = Avalanche_message_two.objects.select_related().all().order_by('-id')
        return render(request, "messages/show-avalanche-message.html", locals())

    messages = Avalanche_message_two.objects.select_related().filter(message_on__date=today_date).order_by('-id')
    return render(request, "messages/show-avalanche-message.html", locals())



@login_required(login_url='/login/')
def show_avalanche_csv_logs(request):
    if cache.get("log_messages"):
        logs_message = cache.get("log_messages")
    else:
        logs = avalanche_message_logs.objects.all()
        logs_message = []
        for i in logs:
            logs_message.append(i.message)
            i.delete()
        cache.set("log_messages", logs_message, timeout=10000)

    return render(request, "csv/avalanche_logs.html", locals())






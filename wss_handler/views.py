import time
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from dashboard.services.wss_log import wss_login_required
from .forms import wss_session_form
from .models import Websocket_Status, message_backup
from .models import ws_sessions, Avalanche_message_one, Avalanche_message_two
import datetime
from .services.natsata_connector import natsat_connector
from datetime import datetime
from dashboard.models import wss_auth_user
from django.contrib.auth.hashers import check_password
import asyncio
from .serializers import ws_auth_serializer, message_ack_serializer


def socket_data():
    if cache.get("websocket_auth"):
        return cache.get("websocket_auth")
    else:
        return False


def socket_authentication(request):
    try:
        w_auth = Websocket_Status.objects.last()
        if w_auth.is_run is True:
           return JsonResponse({"message": "connected"})
        return JsonResponse({"message": "connection failed"})
    except Exception as e:
        return JsonResponse({"message": "connection failed"})



def wss_auth(request):
    websocket_auth = True
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST['password']


        if wss_auth_user.objects.filter(username=username).exists():
            user = wss_auth_user.objects.get(username=username)
            if check_password(password, user.password):
                request.session["wss-auth-username"] = user.username
                request.session["wss-auth-password"] = password
                return redirect("/wss/dashboard/")
            else:
                invalid = True
                message = "invalid password"
        else:
            invalid = True
            message = "invalid username"

    return render(request, "dashboard/pages-login.html", locals())



@wss_login_required(redirect_to="/wss/login/")
def ws_dashboard(request):
    wss_auth_data = ws_sessions.objects.last()
    ws_status = Websocket_Status.objects.last()
    return render(request, "sockets/dashboard.html", locals())

@wss_login_required(redirect_to="/wss/login/")
def ws_connect(request):
    ws_status = Websocket_Status.objects.last()
    if ws_status.is_run is True:
        return redirect("/wss/dashboard/")
    if request.method == "POST":
        ws_form = wss_session_form(request.POST)
        if ws_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            packet_id = request.POST['packet_id']

            if ws_status.is_run:
                print("already connected")
                already_connected = True
            else:
                try:
                  host_name = request.get_host()
                  natsat_connector(username, password, packet_id, host_name)
                  time.sleep(5)
                  run_data = Websocket_Status.objects.last()
                  if run_data.is_run is True:
                      return redirect("/wss/dashboard/")
                  not_connected = True
                except Exception as e:
                    print(e)
            ws_form = wss_session_form()

    return render(request, "sockets/new-connection.html", locals())

@wss_login_required(redirect_to="/wss/login/")
def ws_connection_history(request):
    w_auth = ws_sessions.objects.all()
    return render(request, "sockets/connection-history.html", locals())



@wss_login_required(redirect_to="/wss/login/")
def ws_logout(request):
    # logout_wss.delay()
    run_data = Websocket_Status.objects.last()
    run_data.is_run = False
    run_data.closed_at = datetime.now()
    run_data.save()
    ws_session = ws_sessions.objects.last()
    ws_session.logout_on = datetime.now()
    ws_session.logout = True
    ws_session.save()
    return redirect("/wss/dashboard/")



@wss_login_required(redirect_to="/wss/login/")
def wss_dashboard_logout(request):
    del request.session["wss-auth-username"]
    del request.session["wss-auth-password"]
    return redirect("/wss/login/")






class wss_login_success_create(generics.CreateAPIView):
    serializer_class = ws_auth_serializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ws_auth_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")
            session_id = serializer.validated_data.get("session_id")
            packet_id = serializer.validated_data.get("packet_id")
            log_message = serializer.validated_data.get("log_message")
            try:
                if log_message == "logout":
                    run_data = Websocket_Status.objects.last()
                    run_data.is_run = False
                    run_data.closed_at = datetime.now()
                    run_data.save()
                    ws_session = ws_sessions.objects.last()
                    ws_session.logout_on = datetime.now()
                    ws_session.logout = True
                    ws_session.save()
                else:
                    ws_sessions.objects.create(
                        session_id=session_id,
                        username=username,
                        password=password,
                        packet_id=packet_id,
                        log_message="login successfully"
                    )
                    ws_status = Websocket_Status.objects.last()
                    ws_status.is_run = True
                    ws_status.started_at = datetime.now()
                    ws_status.save()
            except Exception as e:
                print(e)
            return Response("ok")



class message_ack(generics.CreateAPIView):
    serializer_class = message_ack_serializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = message_ack_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            sequence_num = serializer.validated_data.get("sequence_num")
            packet_id = serializer.validated_data.get("packet_id")
            try:
                if packet_id == 5:
                    today_date = datetime.now().date()
                    data = Avalanche_message_one.objects.filter(sequence_num=sequence_num, message_on__date=today_date).last()
                    data.ack = True
                    data.save()
            except:
                return Response("sequence num is invalid")
            return Response("ok")

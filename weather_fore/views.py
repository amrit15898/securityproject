import time
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
import ast
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from taskapp.models import weather_forecast_code
from taskapp.services.weather_forecast import weather_forecast
from wss_handler.models import Weather_Forecast_Message
from dashboard.services.admin_decorator import admin_required
from .forms import *
from .models import weather_grids, weather_forecast_logs
from .services.area_update import area_update
from .services.code_csv import weather_code_csv
from .services.code_update import weather_code_updator
from .services.grid_csv import grid_csv
from django.http import JsonResponse
from weather_fore.services.weather_forecast import weather_obj
from taskapp.views import wss_check
# Create your views here.

weather_kwargs = {
    "sent": False
}
@login_required(login_url="/login/")
def send_weather_forecast(request):
    global weather_kwargs
    weather_codes = weather_forecast_code.objects.all()
    if request.method == 'POST':
        if wss_check() is False:
            message_status_fail = True
            return render(request, "messages/send-weather-forecast.html", locals())
        start_date = request.POST['start-date']
        grid_id = request.POST['grid-id']
        num_of_forecast_day = request.POST['num-of-forecast-day']
        forecast_area = request.POST['forecast-area']
        day_1 = request.POST.get('day-1')
        if day_1 is None:
            day_1=''
        day_2 = request.POST.get('day-2')
        if day_2 is None:
            day_2=''
        day_3 = request.POST.get('day-3')
        if day_3 is None:
            day_3=''
        day_4 = request.POST.get('day-4')
        if day_4 is None:
            day_4=''
        day_5 = request.POST.get('day-5')
        if day_5 is None:
            day_5=''
        day_6 = request.POST.get('day-6')
        if day_6 is None:
            day_6=''
        current_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        format_date = datetime.strftime(current_date, "%d%m%y")
        weather_forecast(request.user, format_date, grid_id, num_of_forecast_day, forecast_area, day_1, day_2, day_3, day_4, day_5, day_6)

        weather_kwargs["sent"] = True
        return redirect("/weather/send-weather-forecast/")
    if weather_kwargs["sent"] is True:
        sent = True
        weather_kwargs["sent"] = False
    return render(request, "messages/send-weather-forecast.html", locals())


@login_required(login_url="/login/")
def show_send_weather(request):
    date = datetime.now().date()
    if request.GET.get("search-date"):
        date = request.GET.get("search-date")
    elif request.GET.get("search-data"):
       messages = Weather_Forecast_Message.objects.all()
       return render(request, "messages/show-send-weather.html", locals())

    messages = Weather_Forecast_Message.objects.filter(send_on__date=date)
    return render(request, "messages/show-send-weather.html", locals())




area_update_kwargs = {
    "send_status": None
}


@login_required(login_url="/login/")
def weather_area_update(request, **kwargs):
    global area_update_kwargs
    if request.method == "POST":
        form = weather_area_update_form(request.POST)
        if wss_check() is False:
            message_status_fail = True
            return render(request, "messages/weather-area-update.html", locals())
        if form.is_valid():
            grid_id = request.POST['grid_id']
            action_code = form.cleaned_data['action_code']
            area_id = form.cleaned_data['area_id']
            area_name = form.cleaned_data['area_name']
            message_status = area_update(
                user=request.user,
                grid_id=grid_id,
                action_code=action_code,
                area_id=area_id,
                area_name=area_name
            )
            if message_status:
                form = weather_area_update_form()
                area_update_kwargs['send_status'] = True
                return redirect("/weather/area-update/")
            else:
                area_update_kwargs['send_status'] = False
    try:
        if area_update_kwargs['send_status'] is True:
            message_status = True
        elif area_update_kwargs['send_status'] is False:
            message_status = False
        area_update_kwargs['send_status'] = None
    except Exception as e:
        print(e)
    return render(request, "messages/weather-area-update.html", locals())


@login_required(login_url="/login/")
def weather_area_update_view(request):
    date = datetime.now().date()
    if request.GET.get("search-date"):
        date = request.GET.get("search-date")
    elif request.GET.get("search-data"):
       messages = weather_area_update_message.objects.all()
       return render(request, "weather-forecast/show-area-update.html", locals())

    messages = weather_area_update_message.objects.filter(send_on__date=date)
    return render(request, "weather-forecast/show-area-update.html", locals())


code_update_kwargs = {
    "message_status": None
}

@login_required(login_url="/login/")
def weather_code_update(request):
    global code_update_kwargs


    if request.method == "POST":
       form = weather_code_update_form(request.POST)
       if wss_check() is False:
           message_status_fail = True
           return render(request, "messages/weather-code-update.html", locals())
       if form.is_valid():
          action_code = form.cleaned_data['action_code']
          avalanche_code = form.cleaned_data['avalanche_code']
          code_details = form.cleaned_data['code_details']
          message_status = weather_code_updator(
              user=request.user,
              action_code=action_code,
              avalanche_code=avalanche_code,
              code_details=code_details
          )
          if message_status is True:
              code_update_kwargs["message_status"] = True
              form = weather_code_update_form()
              return redirect("/weather/code-update/")
          else:
              code_update_kwargs["message_status"] = False
    try:
        if code_update_kwargs['message_status'] is True:
            message_status = True

        code_update_kwargs['message_status'] = None
    except Exception as e:
        print(e)
    return render(request, "messages/weather-code-update.html", locals())


@login_required(login_url="/login/")
def view_weather_code_update(request):
    date = datetime.now().date()
    if request.GET.get("search-date"):
        date = request.GET.get("search-date")
    elif request.GET.get("search-data"):
        messages = weather_code_update_message.objects.all()
        return render(request, "weather-forecast/show-code-update.html", locals())

    messages = weather_code_update_message.objects.filter(send_on__date=date)
    return render(request, "weather-forecast/show-code-update.html", locals())




@admin_required(login_url="/login/")
def add_grid(request):
    if request.method == 'POST':
        form = weather_grid_form(request.POST)
        form2 = grids_form(request.POST)
        if form.is_valid() and form2.is_valid():
            f = form.save()
            grids = form2.cleaned_data['grid_id']
            print(grids)
            for i in grids:
               g = Grids.objects.create(grid_id=i)
               f.natsat_grids.add(g)
            f.save()
            form = weather_grid_form()
            form2 = weather_grid_form()

            added = True
    return render(request, "weather-forecast/add-grid.html", locals())


@admin_required(login_url="/login/")
def view_all_grids(request):
    if request.method == "POST":
        update_id = request.POST['update_id']
        instance = get_object_or_404(weather_grids, id=update_id)
        form = weather_grid_form_update(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            updated = True
        else:
            not_update = True
    elif request.GET.get("delete"):
        id = request.GET.get("delete")
        w = weather_grids.objects.get(id=id)
        w.natsat_grids.all().delete()
        w.delete()
        return redirect("/weather/view-grids/")

    grids = weather_grids.objects.all()
    return render(request, "weather-forecast/view-all-grids.html", locals())

@admin_required(login_url="/login/")
def add_weather_code(request):
    if request.method == "POST":
        form = code_form(request.POST)
        if form.is_valid():
            form.save()
            added = True
            form = code_form()
    return render(request, "weather-forecast/add-code.html", locals())

@admin_required(login_url="/login/")
def view_weather_code(request):
    if request.method == "POST":
        update_id = request.POST['update_id']
        instance = get_object_or_404(weather_codes, id=update_id)
        form = code_form(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            updated = True
            form = code_form()
        else:
            not_update = True
    if request.GET.get("delete"):
        id = request.GET.get("delete")
        weather_codes.objects.get(id=id).delete()
        request.session["deleted"] = True
        return redirect("/weather/view-code/")
    if "deleted" in request.session:
        deleted = True
        del request.session["deleted"]
    codes = weather_codes.objects.all()
    return render(request, "weather-forecast/view-all-code.html", locals())


@admin_required(login_url="/login/")
def grid_add_by_csv(request):
    insert_csv = True
    if request.method == "POST":
        file = request.FILES['file']
        cache.set("weather-grid-csv", file, timeout=10000)
        return render(request, "weather-forecast/grid-csv-data.html", locals())

    return render(request, "weather-forecast/add-grid.html", locals())



def grid_add_csv_reader(request):
    if cache.get("weather-grid-csv"):
        data = grid_csv.file_read(file=cache.get("weather-grid-csv"))
        cache.delete("weather-grid-csv")
        return JsonResponse(data, safe=False)

    else:
        return redirect("/weather/add-grid-by-csv/")



@login_required(login_url="/login/")
def weather_file_csv(request):
    csv_file = True
    if request.method == "POST":
        file = request.FILES['weather-file']
        cache.set("weather-send-csv", file, timeout=10000)
    return render(request, "weather-forecast/message-csv-data.html", locals())



@csrf_exempt
def weather_csv_read(request):
    if request.method == "POST":
        data = request.POST['packets']
        list_data = ast.literal_eval(data)
        response = []
        for i in list_data:
            status = weather_forecast(request.user, i["start_date"], i['grid_id'], i['num_of_day'], i['forecast_area'], i['day_1'], i['day_2'], i['day_3'], i['day_4'], i['day_5'], i['day_6'])
            response.append({
                "id": i['id'],
                "status": status
            })
        return JsonResponse(response, safe=False)
    try:
        file = cache.get("weather-send-csv")
        try:
          file_data = weather_obj.csv_read(file=file)
          return JsonResponse(file_data, safe=False)
        except Exception as e:
            print(e)
        return JsonResponse("invalid", safe=False)

    except Exception as e:
        print(e)
        return JsonResponse("invalid file", status=404)

@csrf_exempt
def weather_grid_validate(request):
    if request.method == "POST":
        grid = request.POST['grid_id']
        if Grids.objects.filter(grid_id=grid).exists():
            return JsonResponse("ok", safe=False)
        else:
            return JsonResponse("bad", safe=False, status=400)



@csrf_exempt
def weather_area_validate(request):
    if request.method == "POST":
        area_id = request.POST['area_id']
        if weather_grids.objects.filter(forecast_area=area_id).exists():
            return JsonResponse("ok", safe=False)
        else:
            return JsonResponse("bad", safe=False, status=400)

def weather_forecast_log(request):
    logs = weather_forecast_logs.objects.all()
    response = []
    for i in logs:
        response.append(i.message)
        i.delete()
    return JsonResponse(response, safe=False)




@admin_required(login_url="/login/")
def upload_code_csv(request):
    insert_csv = True
    if request.method == "POST":
        file = request.FILES['file']
        cache.set("weather-code-csv", file, timeout=10000)
        try:
            df = pd.read_csv(file)
            for index, row in df.iterrows():
                name = row['Forecast']
                code = row['Code']
                relation = row['Relation in Character']
                intensity = row['Intensity']
                area = row['Area']
                legend = row["Legend"]
                break
        except Exception as e:
            print(e)
            invalid_csv = True
            cache.delete("weather-code-csv")
            return render(request, "weather-forecast/add-code.html", locals())

    return render(request, "weather-forecast/code-csv-data.html", locals())


@csrf_exempt
def code_csv_reader(request):
    try:
        file = cache.get("weather-code-csv")
        data = weather_code_csv(excel=file)
        return JsonResponse(data, safe=False)
    except Exception as e:
        print(e)
    return JsonResponse({"status": "File not found please upload"}, safe=False)




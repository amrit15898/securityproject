from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import *
from dashboard.services.admin_decorator import admin_required
from .models import Station, Equation



# Create your views here.


@admin_required(login_url="/login/")
def add_station(request):
    if request.method == "POST":
        form = station_form(request.POST)
        check = request.POST.getlist("check")
        sensor_name = request.POST.getlist("sensor_name")
        unit = request.POST.getlist("unit")
        equation = request.POST.getlist("equation")
        print(sensor_name)
        if form.is_valid():

            # station = form.save()
            print(check)
            print(sensor_name[0])
            print(unit)
            print(equation)

            for sen_id, sen_name, sen_unit, sen_equ in zip(check, sensor_name, unit, equation):
                print(sen_id, sen_name, sen_unit, sen_equ)
                # Sensors.objects.create(
                #     station=station,
                #     sensor_id=sen_id,
                #     sensor_name=sen_name,
                #     unit=sen_unit,
                #     equation=sen_equ
                # )

            form = station_form()
            added = True
    equation = Equation.objects.all()
    range_form = range(23)
    return render(request, "station/add-station.html", locals())

@admin_required(login_url="/login/")
def view_all_station(request):
    station = Station.objects.all()
    return render(request, "station/view-all-station.html", locals())




@admin_required(login_url="/login/")
def station_sensor_equation(request):
    if request.method == "POST":
        form = equation_form(request.POST)
        if form.is_valid():
            form.save()

    equation = Equation.objects.all()
    return render(request, "station/equations.html", locals())


from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Notifications
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from taskapp.models import avalanche_grid

def view_notification(request):

    noti = Notifications.objects.all().order_by('-id')[:5]
    data = []
    today = datetime.now().date().strftime("%d-%m-%Y")
    for i in noti:
        date = i.notification_on+timedelta(hours=5, minutes=30)
        if today == date.date().strftime("%d-%m-%Y"):
            d = "Today"

        else:
            d = date.date().strftime("%d-%m-%Y")
        data.append({
            "info": i.message,
            "date": d,
            "time": date.time().strftime("%H:%M:%S"),
            "noti_for": i.noti_for
        })
    return JsonResponse(data, safe=False)




def notification_counter(request):
    noti_count = Notifications.objects.all().count()
    return JsonResponse({"noti": noti_count})



@login_required(login_url='/login/')
def view_all_notification(request):
    messages = Notifications.objects.all()
    return render(request, "dashboard/view-all-notification.html", locals())

@csrf_exempt
def avalanche_grid_validator(request):
    if request.method == "POST":
        grid_id = request.POST['grid_id']
        if avalanche_grid.objects.filter(grid_id=grid_id).exists():
            return JsonResponse("ok", safe=False)
        else:
            return JsonResponse("bad", safe=False, status=400)



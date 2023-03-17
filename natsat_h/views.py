from django.shortcuts import render
from wss_handler.models import observatory_data
# Create your views here.


def show_observatory_message(request):

    return render(request, "natsat-h/observatory_data.html", locals())




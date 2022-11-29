
from django.urls import path, include
from home.views import *

urlpatterns = [

    path("post-app", post_appointment, name="appointment"),
    path("show-request", show_request, name="showrequest"),
    path("show-emp-request", employee_request, name="employeerequest"),
    path("show-full-request", show_full_request, name="showfull"),
    path("security-panel", security_officer, name="securitypanel"),
    path("full-detail/<id>", full_security_detail, name="fulldetail"),
    path("cancel-request/<id>", cancel_request, name="cancelrequest")


]

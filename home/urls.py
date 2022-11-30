
from django.urls import path, include
from home.views import *

urlpatterns = [

    path("postapntent", post_appointment, name="appointment"),
    path("shsfsdfow-readfafquest", show_request, name="showrequest"),
    path("seret", employee_request, name="employeerequest"),
    path("sfr/312/dfad/<id>", show_full_request, name="showfull"),
    path("sesdfpnel", security_officer, name="securitypanel"),
    path("fd452de/<id>", full_security_detail, name="fulldetail"),
    path("ccdnl1e/23st/<id>", cancel_request, name="cancelrequest"),
    path("clrrkests", cleare_clearance_list, name="clearlist")


]

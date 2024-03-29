
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
    path("clrrkests", cleare_clearance_list, name="clearlist"),
    path("updtap/<id>", update_appointment, name="updateapp"),
    path("forgotpass", forgot_password, name="forgotpass"),
    path("cfhadf-regfsa/<int:id>", reson_unopproved, name="cancelreason"),
    path("undnfadfda", cancel_employee_request, name="unapproved"),
    path("sfohfdoafca/<id>", show_cancel_reason, name="showcancel" ),
    path("showwhistssot/<emp_id>", show_employee_history, name="showhistory"),
    path("hsowfulluser/<int:id>", show_full_user_detail, name="showuser"),
    path("dpanellsf", department_panel, name="dpanel"),
    path("hwpanel" , hw_panel, name="hwpanel"),
    path("oicpanel", oic_panel, name="oicpanel"),
    path("pvtemp", pvt_employee_reqeust, name="pvtemp") ,
    path("cloaseadfcleareas/<id>", close_clearance_reason, name="closereason")
]

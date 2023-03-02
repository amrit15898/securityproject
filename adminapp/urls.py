
from django.urls import path, include
from adminapp.views import *

urlpatterns = [
    path("", admin_panel, name="adminpanel"),
    path("delete-user/<id>", delete_user, name="deleteuser"),
    path("klsdfdkjfadjfadjfad/<id>", update_user, name="updateuser"),
    path("addffadfsfdsf", add_user, name="adduser"),
    path("ffadsfadfadffs", add_department, name="adddep"),
    path("login", login_front_page, name="login"),
    path("logout", logout_handle, name="logout"),
    path("sfdddaf", show_full_department,name="showdepartment"),
    path("suhrs", show_users, name="showusers"),
    path("saappnemt", show_all_appointments,name="showapp"),
    path("dase/2e/7dessfdt/<id>", delete_department, name="deletedepartment"),
    path("udepte/<id>", update_department, name="updatedep"),
    path("check", check_template, name="updatedep"),
    path("formtghfaaf", forgot_message_request, name="forgotmessage"),
    path("cdfapass/<id>", change_password, name="changepass"),
    path("fu-flr", full_profile, name="fullprofile"),
    path("changemppas", change_employee_password, name="chngpassword"),
    path("login-option", login_option, name="loginoption")
]

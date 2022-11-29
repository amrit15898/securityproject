
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
    path("show-users", show_users, name="showusers"),
    path("show_all_appointments", show_all_appointments,name="showapp"),
    path("dase2e7dessfdt/<id>", delete_department, name="deletedepartment"),
    path("update-department/<id>", update_department, name="updatedep")
]

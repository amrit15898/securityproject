
from django.urls import path, include
from adminapp.views import *

urlpatterns = [
    path("", admin_panel),
    path("delete-user/<id>", delete_user, name="deleteuser"),
    path("klsdfdkjfadjfadjfad/<id>", update_user, name="updateuser"),
    path("addffadfsfdsf", add_user, name="adduser"),
    path("ffadsfadfadffs", add_department, name="adddep"),
    path("login", login_front_page, name="login"),
    path("logout", logout_handle, name="logout")
]

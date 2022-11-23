
from django.urls import path, include
from adminapp.views import *

urlpatterns = [
    path("", admin_panel),
    path("delete-user/<id>", delete_user, name="deleteuser"),
    path("update-user/<id>", update_user, name="updateuser"),
    path("add-user", add_user, name="adduser"),
    path("add-department", add_department, name="adddep"),
    path("login", login_front_page, name="login")
]

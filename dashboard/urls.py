from django.urls import path, include
from .import views
from .views import view_user_kwargs, wss_user_kwargs, axis_added_kwargs

urlpatterns = [
    path("", views.Dashboard, name="home page"),
    path("add-pointer/", views.Add_Pointer, name=" create pointer"),
    path('pointer/', include([
        path("<int:id>/", views.pointer),
        path("update/<int:update_id>/", views.pointer),
        path("", views.pointer),
    ])),
    path("login/", include([
        path("", views.Login, name="login-page"),
        path("<websocket_auth>/", views.Login, name="login-page"),
    ])),
    path("logout/", views.Logout, name="logout-page"),
    path("view-all-users/", include([
        path("", views.view_all_user, name="view_all_user", kwargs=view_user_kwargs),
        path("delete/<int:delete_id>/", views.view_all_user, name="delete_user"),
        path("update/<int:update_id>/", views.view_all_user, name="update_user"),
    ])),
    path("add-new-user/", views.add_new_user, name="add-new-user"),
    path("user-profile/", include([
        path("", views.user_profile, name="user-profile"),
        path("edit/<int:update_id>/", views.user_profile, name="user-profile-update"),
    ])),
    path("wss-user/", include([
        path("add/", views.add_wss_user),
        path("view/", views.view_all_wss_user, kwargs=wss_user_kwargs),
        path("delete/<int:id>/", views.delete_wss_user),
    ])),
    path("user-activity/", views.user_activity_cal),
    path("add-avalanche-axis/", views.add_avalanche_axis, kwargs=axis_added_kwargs),
    path("update-avalanche-axis/<int:axis_id>/", views.update_avalanche_axis_code),
    path("view-avalanche-axis-code/", include([
        path("", views.show_avalanche_axis_code),
        path("delete/<int:delete_id>/", views.show_avalanche_axis_code),
    ])),
    path("add-avalanche-axis-csv/", views.add_avalanche_axis_csv),
    path("avalanche-axis-csv-data/", views.avalanche_axis_csv_data),
]

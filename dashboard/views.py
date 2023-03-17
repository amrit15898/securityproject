import json

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, redirect,  HttpResponse
from .models import Pointers, wss_auth_user
from .form import pointer_form, user_form, user_update_form, add_wss_form, avalanche_axis_form, \
    update_avalanche_axis_form
from .models import user_activity
import asyncio
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from dashboard.services.admin_decorator import admin_required
import folium
import os
from folium.plugins import MousePosition
from folium import plugins
from folium.features import DivIcon
from dashboard.services.lat_log import map_data
from django.contrib.auth.hashers import make_password
from taskapp.models import avalanche_axis, avalanche_grid
from .services.axis_add_csv_read import axis_add_csv

# css file
folium.folium._default_css.append(('leaflet_css', '/static/folium/leaflet.css'))
folium.folium._default_css.append(('bootstrap_css', '/static/folium/bootstrap.css'))
folium.folium._default_css.append(('bootstrap_theme_css', '/static/folium/bootstrap_theme.css'))
folium.folium._default_css.append(('awesome_markers_font_css', '/static/folium/font-awesome.min.css'))
folium.folium._default_css.append(('awesome_markers_css', '/static/folium/leaflet.awesome-markers.css'))
folium.folium._default_css.append(('awesome_rotate_css', '/static/folium/leaflet.awesome.rotate.css'))
folium.folium._default_css.append(('draw_css', '/static/folium/draw.css'))
folium.folium._default_css.append(('MousePosition_min_css', '/static/folium/L.Control.MousePosition.min.css'))
folium.folium._default_css.append(('measure_min-css', '/static/folium/leaflet-measure.min.css'))

# js file
folium.folium._default_js.append(('leaflet', '/static/folium/leaflet.js'))
folium.folium._default_js.append(('jquery', '/static/folium/jquery.js'))
folium.folium._default_js.append(('bootstrap', '/static/folium/bootstrap.js'))
folium.folium._default_js.append(('awesome_markers', '/static/folium/markers.js'))
folium.folium._default_js.append(('leaflet_draw', '/static/folium/draw.js'))
folium.folium._default_js.append(('Control_MousePosition_min', '/static/folium/L.Control.MousePosition.min.js'))
folium.folium._default_js.append(('measure_min', '/static/folium/measure.min.js'))





def Login(request, websocket_auth=False):
    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("/")
        else:
            invalid = True
            return render(request, "dashboard/pages-login.html", locals())

    if request.user.is_authenticated:
        return redirect("/")
    return render(request, "dashboard/pages-login.html", locals())


def Logout(request):
    logout(request)
    return redirect("/login")


@login_required(login_url='/login/')
def home(request):
    shp_dir = os.path.join(os.getcwd(), 'media', 'mapdata')
    m = folium.Map(location=[25.5464, 78.5742], zoom_start=5, height=620,)
    style_basin = {'fillColor': '#228B22', 'color': '#228B22'}
    style_river = {'color': 'blue'}
    folium.GeoJson(os.path.join(shp_dir, 'states_india.geojson'), name='basin',
                   style_function=lambda x: style_basin).add_to(m)

    img = os.path.join(shp_dir, "test.jpg")

    # image = folium.raster_layers.ImageOverlay(
    #     name="Permafrost",
    #     image=img,
    #     bounds=[[110, 100], [110, 100]],
    #     interactive=True,
    #     zindex=1,
    # )
    # image.add_to(m)
    popup1 = folium.LatLngPopup()
    m.add_child(popup1)
    # mouser hover Coordinates
    formatter = "function(num) {return L.Util.formatNum(num, 5) + ' º ';};"
    MousePosition(
        position="topright",
        separator=" | Lon ",
        empty_string="NaN",
        lng_first=True,
        num_digits=20,
        prefix="Coordinates: Lat",
        lat_formatter=formatter,
        lng_formatter=formatter,
    ).add_to(m)
    # marker
    # markers = Pointers.objects.filter(point_type="marker")
    #
    # try:
    #     for j in map_data:
    #         folium.Marker(
    #             location=[j["lat"], j["lon"]],
    #             icon=DivIcon(
    #                 icon_size=(150, 36),
    #                 icon_anchor=(0, 0),
    #                 html='<div style="font-size: 10px; font-weight:bold;">%s</div>' % j["name"],
    #             ),
    #         ).add_to(m)
    #
    # except Exception as e:
    #     print("label not write because of", e)
    markers = Pointers.objects.all()
    for i in markers:
        folium.Marker(
            location=[i.latitude, i.longitude],
            icon=DivIcon(
                icon_size=(150, 36),
                icon_anchor=(0, 0),
                html='<div style="font-size: 10px; font-weight:bold;">%s</div>' % i.title,
            ),
        ).add_to(m)
        if i.point_type == "marker":
            folium.Marker(location=[i.latitude, i.longitude],
                          icon=folium.Icon(color="green")).add_to(m)

    # draw tools
    plugins.Draw(export=True, filename='data.geojson', position='topleft', draw_options=None, edit_options=None).add_to(m)
    #  measure tool
    plugins.MeasureControl(position='topright', primary_length_unit='meters', secondary_length_unit='miles',
                           primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(m)
    folium.LayerControl(m)
    m._id = "1"
    m = m._repr_html_()
    user_activity.objects.create(user=request.user, task_details="map view")
    return render(request, "dashboard/dashboard.html", locals())

@login_required(login_url="/login/")
def Dashboard(request):
    context = {}
    if request.method == "POST":
        select_item = request.POST.getlist("switcher")
        print("select item len is ", len(select_item))
        print(select_item)
        if (len(select_item)==3):
            markers = Pointers.objects.filter(point_type =select_item[0]) | Pointers.objects.filter(point_type=select_item[1]) | Pointers.objects.filter(point_type=select_item[2])       
        if (len(select_item)==2):   
            markers = Pointers.objects.filter(point_type =select_item[0]) | Pointers.objects.filter(point_type=select_item[1]) 
        if(len(select_item) == 1):
            markers = Pointers.objects.filter(point_type = select_item[0])
        context["markers"] = markers
    return render(request, "dashboard/home.html", context)


@login_required(login_url='/login/')
def pointer(request, id=None, update_id=None):
    if id:
        p = Pointers.objects.get(id=int(id))
        p.delete()
        return redirect("/pointer/")

    if request.method == "POST":
        instance = get_object_or_404(Pointers, id=update_id)
        form = pointer_form(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            updated = True
            user_activity.objects.create(user=request.user, task_details=f"add update {form.cleaned_data['title']}")

        else:
            not_add = True

    pointer_data = Pointers.objects.all()
    return render(request, "map/pointer_view.html", locals())


@login_required(login_url='/login/')
def Add_Pointer(request):
    form = pointer_form()
    if request.method == "POST":
        form = pointer_form(request.POST)
        if form.is_valid():
            form.save()
            added = True
            user_activity.objects.create(user=request.user, task_details=f"add pointer {form.cleaned_data['title']}")
        else:
            not_add = True
    return render(request, "map/pointer_add.html", locals())






view_user_kwargs = {
  "updated": False
}

@admin_required(login_url="/login/")
def view_all_user(request, delete_id=None, update_id=None, **kwargs):

    users = User.objects.all().order_by("-id")
    if delete_id:
        user = User.objects.filter(id=delete_id).first()
        user.delete()
        return redirect("/view-all-users/")

    elif update_id:
        usr = get_object_or_404(User, id=update_id)
        form = user_update_form(request.POST or None, instance=usr)
        if form.is_valid():
            form.save()
            view_user_kwargs["updated"] = True
        else:
            view_user_kwargs["not_update"] = True
        return redirect("/view-all-users/")
    else:
        view_user_kwargs["updated"] = False
        view_user_kwargs["not_update"] = False


    if "user_added" in request.session:
        user_added = True
        del request.session["user_added"]

    return render(request, "admin/view-all-user-details.html", locals())


@admin_required(login_url="/login/")
def add_new_user(request):
    if request.method == "POST":
        form = user_form(request.POST)
        if form.is_valid():
            usr = form.save()
            usr.set_password(form.cleaned_data['password'])
            usr.save()
            request.session["user_added"] = True
            return redirect("/view-all-users/")
        else:
            not_valid = True

    return render(request, "admin/add-new-user.html", locals())





@admin_required(login_url='/login/')
def user_profile(request, update_id=None):
    if request.method == "POST" and update_id:
        usr = get_object_or_404(User, id=update_id)
        form = user_update_form(request.POST or None, instance=usr)
        if form.is_valid():
            form.save()
            user_profile_edited = True
            return redirect("/user-profile/")
        else:
            user_profile_edited = False


    # password change
    elif request.method == "POST":
        password = request.POST["password"]
        new_password = request.POST["newpassword"]
        re_new_password = request.POST["renewpassword"]
        user = authenticate(username=request.user, password=password)
        if new_password == re_new_password:
            invalid_password = False
        else:
            invalid_password = True
        if user and invalid_password is False:
            usr = User.objects.get(username=request.user)
            usr.set_password(new_password)
            usr.save()
            login(request, usr)
            changed = True
        else:
            if user is None:
               incorrect = True


    return render(request, "dashboard/user-profile.html", locals())




@admin_required(login_url='/login/')
def add_wss_user(request):
    if request.method == "POST":
        form = add_wss_form(request.POST)
        if form.is_valid():
            usr = form.save()
            usr.password = make_password(usr.password)
            usr.created_by = request.user
            usr.save()
            user_added = True

        else:
            not_valid = True
    return render(request, "admin/add-new-wss-user.html", locals())

wss_user_kwargs = {
    "updated": False,
    "deleted": False
}


@admin_required(login_url="/login/")
def view_all_wss_user(request, **kwargs):
    global wss_user_kwargs
    if request.method == "POST":
        username = request.POST['username']
        if wss_auth_user.objects.filter(username=username).exists():
            user = wss_auth_user.objects.get(username=username)
            form = add_wss_form(request.POST, instance=user)
            if form.is_valid():
               password = request.POST['password']
               user.password = make_password(password)
               user.save()
               wss_user_kwargs["updated"] = True
               return redirect("/wss-user/view/", kwargs = wss_user_kwargs)
            else:
                invalid = True

        else:
            not_valid_username = True
    try:
        if kwargs['updated'] is True:
            updated = True
            wss_user_kwargs["updated"] = False
        elif kwargs['deleted'] is True:
            deleted = True
            wss_user_kwargs["deleted"] = False
    except Exception as e:
        pass
    users = wss_auth_user.objects.all()
    return render(request, "admin/view-all-wss-users.html", locals())



@admin_required(login_url="/login/")
def delete_wss_user(request, id):
    global wss_user_kwargs
    try:
        u = wss_auth_user.objects.get(id=id)
        u.delete()
        wss_user_kwargs["deleted"] = True
    except Exception as e:
        print(e)
    return redirect("/wss-user/view/")

@admin_required(login_url="/login/")
def user_activity_cal(request):

    return render(request, 'admin/user-activity.html')


axis_added_kwargs = {"added": False}
@admin_required(login_url="/login/")
def add_avalanche_axis(request, **kwargs):
    global axis_added_kwargs
    if request.method == "POST":
        form = avalanche_axis_form(request.POST)
        if form.is_valid():
           axis = form.cleaned_data['avalanche_axis']
           avalanche_axis_code = form.cleaned_data['avalanche_axis_code']
           aor = form.cleaned_data['aor']
           grids = request.POST['grids']
           axis_code_afg = request.POST['axis_code_afg']
           avalanche_axis.objects.create(
               avalanche_axis=axis,
               avalanche_axis_code=avalanche_axis_code,
               aor=aor,
               grids=grids,
               axis_code_afg=axis_code_afg
           )
           for g in list(grids.split(",")):
               try:
                   avalanche_grid.objects.create(
                       grid_id=g
                   )
               except Exception as e:
                   print(e, "this exception can be ignore")
           axis_added_kwargs["added"] = True
           return redirect("/add-avalanche-axis/")
    if kwargs["added"] is True:
        added = True
        axis_added_kwargs["added"] = False
    return render(request, "admin/add-avalanche-axis.html", locals())

show_kwargs = {"updated": False}
@admin_required(login_url="/login/")
def show_avalanche_axis_code(request, delete_id=None):
    global show_kwargs
    if show_kwargs['updated']:
        updated = True
        show_kwargs['updated'] = False
    if delete_id is not None:
        try:
            data = avalanche_axis.objects.get(id = delete_id)
            data.delete()
            deleted = True
        except Exception as e:
            return redirect("/view-avalanche-axis-code/")

    axis = avalanche_axis.objects.all()
    return render(request, "admin/show-avalanche-axis-code.html", locals())


@admin_required(login_url="/login/")
def update_avalanche_axis_code(request, axis_id):
    try:
        updating = True
        axis = avalanche_axis.objects.get(id=axis_id)
        if request.method == "POST":
            form = update_avalanche_axis_form(request.POST or None, instance=axis)
            if form.is_valid():
                form.save()
                global show_kwargs
                show_kwargs['updated'] = True
                show_avalanche_axis_code()

        return render(request, "admin/add-avalanche-axis.html", locals())
    except Exception as e:
        print(e)
        return redirect("/view-avalanche-axis-code/")



@admin_required(login_url="/login/")
def add_avalanche_axis_csv(request):
    insert_csv = True
    if request.method == "POST":
        file = request.FILES['file']
        cache.set("avalanche-axis-csv", file, timeout=10000)
        return render(request, "admin/avalanche-axis-csv-message.html")

    return render(request, "admin/add-avalanche-axis.html", locals())


from django.http import HttpResponse
def avalanche_axis_csv_data(request):
    try:
        file = cache.get("avalanche-axis-csv")
        data = axis_add_csv(file)
        return JsonResponse(data, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse("something wrong", safe=False)


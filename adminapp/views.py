from django.shortcuts import render,redirect
from home.models import * 
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from home.models import postions
from django.contrib.auth.decorators import login_required
# Create your views here.\
from django.http import HttpResponse

@login_required
def admin_panel(request):
    print(request.user)
    if request.user.is_staff == True:
        users = User.objects.all()
        paginator = Paginator(users, 4)
        page_no = request.GET.get("page")
        userDataFinal = paginator.get_page(page_no)
        departments = Department.objects.all()
        context = {}
        context["users"] = userDataFinal
        context["departments"] = departments
        return render(request, "index.html",context)

    return HttpResponse("this is page not visible for you")

@login_required
def delete_user(request,id):
    try:

        user = User.objects.get(id=id)
        user.delete()
     
        return redirect("/adminpanel")

    except User.DoesNotExist:
        return redirect("/adminpanel")

def update_user(request,id):
    user = User.objects.get(id=id)
    context = {"user": user}
    if request.method =="POST":
        name = request.POST.get("name")
        position = request.POST.get("position")
        password = request.POST.get("password")
        user.name = name 
        user.position = position
        user.password = password 
        user.save(using="default")
        user.save(using="new")
        return redirect("/adminpanel")
    return render(request, "updateuser.html",context)



def add_user(request):
    if request.method=="POST":
        position = request.POST.get("position")
        print(position)
        name = request.POST.get("name")
        password = request.POST.get("password")
        obj = User(position=position, name=name)
        obj.set_password(password)
        obj.save(using="default")
        obj.save(using="new")

    return render(request, "adduser.html")


def add_department(request):
    if request.method == "POST":
        name = request.POST.get("name")
        obj = Department(name=name)
        obj.save(using="default")
        obj.save(using="new")

    
    return render(request, "adddepartment.html")




def login_front_page(request):
    if request.method=="POST":
        name = request.POST.get("name")
        password = request.POST.get("password")
        print(name, password)
        user = authenticate(request, name=name, password = password)

        if user is not None:
            login(request, user)
            print("login hoya")
            print(postions[3][1])
            if request.user.is_superuser == True:
                return redirect("/adminpanel")

            
            if request.user.position == postions[4][1]:
                return redirect("/home/post-app")

            else:
                return redirect("/home/show-request")


        else:
            print("something went wrong")


    return render(request, "login.html")

def logout_handle(request):
    logout(request)
    return redirect("/adminpanel/login")


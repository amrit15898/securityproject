from django.shortcuts import render,redirect
from home.models import * 
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from home.models import postions
from django.contrib.auth.decorators import login_required
# Create your views here.\
from django.http import HttpResponse
from django.contrib import messages

@login_required
def admin_panel(request):
    
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


def delete_user(request,id):
    try:

        user1 = User.objects.using("default").get(id=id)
        user2 = User.objects.using("new").get(id=id)
    
        user1.delete()
        user2.delete()
        return redirect("/adminpanel")

    except User.DoesNotExist:
        return redirect("/adminpanel")

def update_user(request,id):
    user1 = User.objects.using("default").get(id=id)
    user2 = User.objects.using("new").get(id=id)
    context = {"user": user1}

    if request.method =="POST":
        name = request.POST.get("name")
        position = request.POST.get("position")
        password = request.POST.get("password")
        user1.name = name 
        user1.position = position
        user1.password = password 
        user2.name = name 
        user2.position = position
        user2.password = password 
        user2.save(using="default")
        user2.save(using="new")
        return redirect("/adminpanel")
    return render(request, "updateuser.html",context)



def add_user(request):
    

    if request.method=="POST":
        position = request.POST.get("position")
        print(position)
        name = request.POST.get("name")
        password = request.POST.get("password")
        def genrate_id():
            num = 134134 
            obj = User.objects.all().count()
            num+=obj
            return num
        obj = User(position=position, name=name, user_id=genrate_id())
        obj.set_password(password)
        obj.save(using='default')
        obj.save(using='new', force_insert=True)

        return redirect("/adminpanel")
       

    return render(request, "adduser.html")


def add_department(request):
    if request.method == "POST":
        name = request.POST.get("name")
        obj = Department(name=name)
        obj.save(using="default")
        obj.save(using="new")   
        return redirect("/adminpanel")
    return render(request, "adddepartment.html")

def login_front_page(request):
    if request.method=="POST":
        name = request.POST.get("name")
        password = request.POST.get("password")
        obj = User.objects.filter(name=name).first()
        if not obj:
            messages.info(request, "This user is not exit ")
            return redirect("/")
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

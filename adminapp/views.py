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
        user_id = request.POST.get("userid")
        
        obj = User.objects.filter(user_id=user_id).first()
        if obj:
            print("this id is already exits")
            messages.info(request, "User id is exits please enter a different id")
            return redirect("/adminpanel/addffadfsfdsf")
        


        obj = User(position=position, name=name, user_id =user_id)

        obj.set_password(password)
        obj.save(using='default')
        obj.save(using='new', force_insert=True)

        return redirect("/adminpanel")
       

    return render(request, "adduser.html")


def add_department(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            print(name)
            obj = Department.objects.filter(name=name)
            if obj:
                messages.warning(request, "Depeartment already exits")

                return redirect("/")
            obj = Department(name=name)
            obj.save(using= "default")
            obj.save(using="new", force_insert=True)   
            
        except Exception as e:
            messages.warning("something went wrong", + str(e))
            
            return redirect("/adminpanel")
        return redirect("/adminpanel")
    return render(request, "adddepartment.html")

def login_front_page(request):
    if request.method=="POST":
        user_id = request.POST.get("id")
        password = request.POST.get("password")
        obj = User.objects.filter(user_id=user_id).first()
        if not obj:
            messages.info(request, "This user_id is not exit ")
            return redirect("/")
      
        user = authenticate(request, user_id=user_id, password = password)
        if user is not None:
            try:
                login(request, user)
                print("login hoya")
                print(postions[3][1])
                if request.user.is_superuser == True:
                    return redirect("/adminpanel")      
                if request.user.position == postions[4][1]:
                    return redirect("/home/post-app")
                else:
                    return redirect("/home/show-request")
                
            except Exception as e:
                print("something went wrong")
                messages.error(request, "please check your crediantles")
                
        else:
            messages.error(request, "Enter a correct password")
       
    return render(request, "login.html")

def logout_handle(request):
    logout(request)
    return redirect("/adminpanel/login")


def show_full_department(request):
    departments = Department.objects.all()
    context = {"departments": departments}

    return render(request, "department.html", context )


def delete_department(request,id):
    obj = Department.objects.get(id=id)
    obj.delete(using="default")
    obj.delete(using="new")
    messages.success(request, "Department Deleted Successfully")

    return redirect("/")


def show_users(request):
    users = User.objects.all().order_by('id')
    paginator = Paginator(users, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"users": page_obj}
    return render(request, "showalluser.html",context)


def show_all_appointments(request):
    objs = Appointment.objects.all()
    context = {"objs": objs}
    return render(request, "showappointment.html",context)
    

    

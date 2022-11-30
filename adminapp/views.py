from django.shortcuts import render,redirect
from home.models import * 
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from home.models import postions
from django.contrib.auth.decorators import login_required
# Create your views here.\
from django.http import HttpResponse
from django.contrib import messages
from django.http import HttpResponseRedirect

@login_required
def admin_panel(request):
    
    if request.user.is_staff == True:
        try:
            users = User.objects.using("default")
            usercount = User.objects.using("default").count()
        except Exception as e:
            pass
        
        try:
            
            departmentcount = Department.objects.using("new").count()
            appcount = Appointment.objects.using("new").count()       
        except Exception as e:
            print(e)
            
        paginator = Paginator(users, 4)
        page_no = request.GET.get("page")
        userDataFinal = paginator.get_page(page_no)
        departments = Department.objects.all()
        context = {}
        context["users"] = userDataFinal
        context["departments"] = departments
        context["usercount"] = usercount
        context["departmentcount"] = departmentcount
        context["appcount"] = appcount
        return render(request, "index.html",context)
    return HttpResponse("this is page not visible for you")


def delete_user(request,id):
    try:

        try:
            user1 = User.objects.using("default").get(id=id)
            user1.delete()
            messages.success(request, "user deleted successfully")
            return redirect("/adminpanel/suhrs")    
        except Exception as e:         
            pass       
        try:
            user2 = User.objects.using("new").get(id=id)
            user2.delete()
            messages.success(request, "user deleted successfully")
            return redirect("/adminpanel/suhrs")    
        except Exception as e:
            pass


    except User.DoesNotExist:
        messages.warning(request, "something went wrong user not deleted")
        return redirect("/adminpanel/suhrs")

def update_user(request,id):
    try:
        user1 = User.objects.using("default").get(id=id)
        user2 = User.objects.using("new").get(id=id)
        context = {"user": user1}       
        if request.method =="POST":
            name = request.POST.get("name")
            position = request.POST.get("position")
            # password = request.POST.get("password")
            user1.name = name 
            user1.position = position
            # user1.set_password(password) 
            user2.name = name 
            user2.position = position
            # user2.set_password(password)
            try:
                user2.save(using="default")
            except Exception as e:
                pass
            try:
                user2.save(using="new")
            except Exception as e:
                pass
            return redirect("/adminpanel")
    except Exception as e:
        print(e)
        messages.info(request, "something went wrong")
        return HttpResponseRedirect(request.path_info)

    return render(request, "updateuser.html",context)



def add_user(request):
    departments = Department.objects.all()
    context = {"departments": departments}
    if request.method=="POST":
        position = request.POST.get("position")

        name = request.POST.get("name")
        password = request.POST.get("password")
        user_id = request.POST.get("userid")
        
        obj = User.objects.filter(user_id=user_id).first()

        if not name:
            messages.info(request, "name should  not be blank")
            return redirect("/adminpanel/addffadfsfdsf")
        if obj:
         
            messages.info(request, "User id is exits please enter a different id")
            return redirect("/adminpanel/addffadfsfdsf")

        if position == "selectposition":
            messages.info(request, "please select the position")
            return redirect("/adminpanel/addffadfsfdsf")
        
        if not password:
            messages.info(request, "password required")
            return redirect("/adminpanel/addffadfsfdsf")
        
        if not user_id:
            messages.info(request, "please enter a id")
            return redirect("/adminpanel/addffadfsfdsf")

        obj = User(position=position, name=name, user_id =user_id)

        obj.set_password(password)
        try:
            obj.save(using='default')
        except Exception as e:
            pass       
        try:
            obj.save(using='new', force_insert=True)
        except Exception as e:
            pass
        return redirect("/adminpanel")
    return render(request, "adduser.html", context)

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
            try:
                obj.save(using= "default")              
            except Exception as e:
                pass
            try:               
                obj.save(using="new", force_insert=True)   
            except Exception as e:
                print(e)           
        except Exception as e:
            messages.warning("something went wrong", + str(e))
            
            return redirect("/adminpanel")
        return redirect("/adminpanel")
    return render(request, "adddepartment.html")

def update_department(request, id):
    dep1 = Department.objects.using("default").get(id=id)
    dep2 = Department.objects.using("new").get(id=id)
    context = {
        "dep": dep1
    }
    if request.method=="POST":
        name = request.POST.get("name")
        dep1.name= name
        dep2.name = name 
        try:
            dep1.save()        
        except Exception as e:
            pass
        try:        
            dep2.save()
        except Exception as e:
            pass
    return render(request, "adddepartment.html", context)



    

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
                    return redirect("/home/postapntent")

                if request.user.position == postions[5][1]:
                    return redirect("/home/sesdfpnel")
                else:
                    return redirect("/home/shsfsdfow-readfafquest")
                
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
    try:
        departments = Department.objects.using("default")       
    except Exception as e:
        pass    
    try:
        departments = Department.objects.using("new")       
    except Exception as e:
        pass
    context = {"departments": departments}
    return render(request, "department.html", context )


def delete_department(request,id):
    try:
        try:
            obj1 = Department.objects.using("default").get(id=id)
            obj1.delete()         
        except Exception as e:
            pass  
        try:
            obj2 = Department.objects.using("new").get(id=id)
            obj2.delete()
        except Exception as e:
            pass
        
        

    except Exception as e:
        print(e)
        messages.info(request, "something went wrong")
        return redirect("/adminpanel")
    messages.success(request, "Department Deleted Successfully")

    return redirect("/adminpanel")


def show_users(request):
    try:
        users = User.objects.using("default").order_by('id')
    except Exception as e:
        print(e)
    try:
        users = User.objects.using("new").order_by("id")
    except Exception as e:
        print(e)
    paginator = Paginator(users, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"users": page_obj}
    return render(request, "showalluser.html",context)


def show_all_appointments(request):
    try:       
        appointments = Appointment.objects.using("default")

    except Exception as e:
        pass
    try:
        appointments = Appointment.objects.using("new")
    except Exception as e:
        print(e)
    paginator = Paginator(appointments, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"objs": page_obj}
    return render(request, "showappointment.html",context)
    

    

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
    usercount = 0
    appcount = 0
    departmentcount = 0
    departments = {}
    users  = {}
    
    if request.user.is_staff == True:
        try:
            users = User.objects.exclude(is_staff = True)
            usercount = User.objects.all().count()
            departmentcount = Department.objects.using("new").count()
            appcount = Appointment.objects.using("new").count()   
            departments = Department.objects.all()   
            print() 
        except Exception as e:
            messages.error(request, "Something went wrong")

        
        # try:
            
        # except Exception as e:
        #     print(e)
            
        # paginator = Paginator(users, 4)
        # page_no = request.GET.get("page")
        # userDataFinal = paginator.get_page(page_no)
        
        context = {}
        context["users"] = users
        context["departments"] = departments
        context["usercount"] = usercount
        context["departmentcount"] = departmentcount
        context["appcount"] = appcount
        return render(request, "mainpage.html",context)
    return HttpResponse("this is page not visible for you")

@login_required 
def delete_user(request,id):
    try: 
        user1 = User.objects.get(id=id)
  
        user1.delete()
        return redirect("/adminpanel/suhrs")
         
    except User.DoesNotExist:
        messages.warning(request, "something went wrong user not deleted")
        return redirect("/adminpanel/suhrs")
           
    
@login_required
def update_user(request,id):
    try:
        user1 = User.objects.get(id=id)
        context = {"user": user1}       
        if request.method =="POST":
            name = request.POST.get("name")
            user_id = request.POST.get("user_id")
            position = request.POST.get("position")
            # password = request.POST.get("password")
            user1.name = name 
            user1.position = position
            user1.user_id = user_id
            # user1.set_password(password) 
            user1.save()
            # user1.save(using="new")
            return redirect("/adminpanel")
    except Exception as e:
        print(e)
        messages.info(request, "something went wrong")
        return HttpResponseRedirect(request.path_info)
    return render(request, "updateuser.html",context)


@login_required
def add_user(request):
    departments = Department.objects.all()
    context = {"departments": departments}
    if request.method=="POST":
        position = request.POST.get("position")
        name = request.POST.get("name")
        password = request.POST.get("password")
        user_id = request.POST.get("userid")
        image = request.POST.get("image")
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
        obj = User(position=position, name=name, user_id =user_id, image=image)
        obj.set_password(password)
        obj.save()
        # obj.save(using='new', force_insert=True)
        return redirect("/adminpanel")
        
     
    return render(request, "adduser.html", context)
@login_required
def add_department(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            obj = Department.objects.filter(name=name)
            if obj:
                messages.warning(request, "Depeartment already exits")
                return redirect("/")
            obj = Department(name=name)
            obj.save()  
            return redirect("/adminpanel/sfdddaf")        
            # obj.save(using = "new")

        except Exception as e:
            messages.warning(request, "something went wrong", + str(e))   
            return redirect("/adminpanel")

    return render(request, "adddepartment.html")
@login_required
def update_department(request, id):
    try:
        dep1 = Department.objects.using("default").get(id=id)
        dep2 = Department.objects.using("new").get(id=id)
    except Exception as e:
        messages.warning(request, "soemthing went wrong")
    context = {
        "dep": dep1
    }
    if request.method=="POST":
        name = request.POST.get("name")
        dep1.name= name
        dep2.name = name 
        try:
            dep1.save()      
            # dep2.save(using="new")
            return redirect("/adminpanel/sfdddaf")
        except Exception as e:
            pass
    return render(request, "updatedep.html", context)



    

def login_front_page(request):
    if request.method=="POST":
        user_id = request.POST.get("id")
        password = request.POST.get("password")
        if user_id == "":
            messages.warning(request, "please enter a user id") 
        if password == "":
            messages.warning(request, "please enter a password")
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
       
                messages.error(request, "please check your crediantles")             
        else:
            messages.error(request, "Enter a correct password")    
    return render(request, "login.html")



def logout_handle(request):
    logout(request)
    return redirect("/adminpanel/login")


@login_required
def show_full_department(request):

    try:
        departments = Department.objects.all()     
        # departments = Department.objects.using("new")       
    except Exception as e:
        messages.warning(request, "somethign went wrong")
    context = {"departments": departments}
    return render(request, "department.html", context )

@login_required
def delete_department(request,id):
    try:
        obj1 = Department.objects.get(id=id)

        obj1.delete()         
        # obj2.delete()
        return HttpResponseRedirect(request.path_info)
    except Exception as e:
        pass

    
    return redirect("/adminpanel/sfdddaf")
        
    

@login_required
def show_users(request):
    users = {}
    try:
        users = User.objects.exclude(is_staff=True)
        # users = User.objects.all(using = "new")

    except Exception as e:
        print(e)
    context = {"users": users}
    return render(request, "showalluser.html",context)

@login_required
def show_all_appointments(request):
    appointments = {}
    try:       
        appointments = Appointment.objects.all()
        # appointments = Appointment.objects.using("new")
    except Exception as e:
        messages.warning("something went wrong")
   
    context = {"objs": appointments}
    return render(request, "showappointment.html",context)
    


def check_template(request):
    return render(request, "mainpage.html")

@login_required
def forgot_message_request(request):
    objs = ForgetMessageRequest.objects.all()
    context = {"objs": objs}
    return render(request, "forgotrequest.html", context)

def change_password(request, id):
    try:
        obj = User.objects.get(user_id=id)
        if request.method=="POST":
            password = request.POST.get("password")
            obj.set_password(password)
            obj.save()
            return HttpResponseRedirect(request.path_info)
    except Exception as e:
            messages.error(request, "something went wrong")
            return HttpResponseRedirect(request.path_info)
    return render(request, "changepass.html")



    

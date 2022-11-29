from django.shortcuts import render, redirect
from .models import *
from .models import postions
# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
@login_required
def post_appointment(request):

    gh_dh = User.objects.filter(position = "GH/DH")
    tech_dir = User.objects.filter(position = "Tech Director")
    departments = Department.objects.all()
   
    context = {}
    context["gh_dh"] = gh_dh
    context["tech_dir"] = tech_dir
    context["departments"] = departments 
    if request.method=="POST":
        gh_dh = request.POST.get("gh_dh")
        tdir = request.POST.get("tdir")
        date = request.POST.get("date")
        description = request.POST.get("description")
        department = request.POST.get("department")
        dh_gh_clr = request.POST.get("dh_gh_clr")
        tech_dir_clr = request.POST.get("tech_dir_clr")
        ass_dir_clr = request.POST.get("ass_dir_clr")
        dir_clr = request.POST.get("dir_clr")
        
        if gh_dh == "SelectGH":
            messages.warning(request, "Please select Gh")
            return redirect("/home/post-app")
        
        if tdir == "SelectTD":
            messages.warning(request, "Please select tdir")
            return redirect("/home/post-app")

        if department == "SelectDep":
            messages.warning(request, "Please the select the department")
            return redirect("/home/post-app")

        final_gh_dh = User.objects.get(id=gh_dh)
        final_tech_dir = User.objects.get(id=tdir)
        dep = Department.objects.get(id=department)
        obj = Appointment(gh_dh= final_gh_dh, tech_dir =final_tech_dir, description=description, department=dep, date=date)
        obj.r_user = request.user    
        obj.save(using="default")
        obj.save(using="new", force_insert=True)

        return redirect("/home/show-emp-request")
      
    return render(request, "clearance.html", context)


@login_required
def show_request(request):

    try:
        user = request.user   
        context = {}
  
        if request.user.position == postions[3][1]:
   
            objs = Appointment.objects.using("default").filter(gh_dh__name=request.user)

    
        elif request.user.position == postions[2][1]:
            objs = Appointment.objects.using("default").filter(tech_dir__name = request.user)


        elif request.user.position == postions[0][1]:
            objs = Appointment.objects.all()
        elif request.user.position == postions[1][1]:
            objs = Appointment.objects.all()    

        context["objs"] = objs

    
        if 'approved' in request.POST:
            value = request.POST.get("approved")
            obj = Appointment.objects.get(id=value)
  
            position = request.user.position
       
            if (position == postions[3][1]):
                obj.dh_gh_clr = "Approved"
                obj.save()
                    
            if position == postions[2][1]:
                obj.tech_dir_clr = "Approved"
                obj.save()
            if position == postions[0][1]:
            
                obj.dir_clr = "Approved"
                obj.save()
            if position == postions[1][1]:
                obj.ass_dir_clr = "Approved"
                obj.save()
         
        if 'napproved' in request.POST:
            value = request.POST.get("napproved")     
            obj = Appointment.objects.get(id=value)
            position = request.user.position    
            if (position == postions[3][1]):
                print("gh called")
                obj.dh_gh_clr = "Not Approved"
                obj.save()
                    
            if position == postions[2][1]:
                print("gh called")
                obj.tech_dir_clr = "Not Approved"
                obj.save()
            if position == postions[0][1]:
                print("Associate director")
                obj.dir_clr = "Not Approved"
                obj.save()
            if position == postions[1][1]:
                print("director")
                obj.ass_dir_clr = "Not Approved"
                obj.save     

        if "forward" in request.POST:
            print("running")
            value = request.POST.get("forward")
            print(value)
            obj = Appointment.objects.get(id=value)
            print(obj)
            obj.send_security = True
            obj.save()
            

   
        return render(request, "ghtechdir.html",context)

    except Exception as e:
        return render(request, "ghtechdir.html")




def employee_request(request):
    objs = Appointment.objects.filter(r_user = request.user)
    context = {"objs": objs}
    return render(request, "emprequest.html",context)


def show_full_request(request):
    return render(request, "fulldetail.html")


def department_head(request):
    clr_appointments = Appointment.objects.filter(dir_clr="Approved") | Appointment.objects.filter(gh_dh=request.user)
    context = {"apointments": clr_appointments}

    return render(request, "departmenthead.html", context)

def security_officer(request):
    try:
        objs = Appointment.objects.filter(send_security=True)
        context = {"objs": objs}
    except Exception as e:
        print(e)
    return render(request, "security.html", context)


def full_security_detail(request,id):
    try:
        obj = Appointment.objects.get(id=id)
        context = {"obj": obj}


    except Exception as e:
        messages.warning(request, "something went wrong")
        return redirect("/home/security-panel")

    return render(request, "fullsecurity.html", context)


def cancel_request(request, id):
    try:
        obj1 = Appointment.objects.using("default").get(id=id)
        obj2 = Appointment.objects.using("new").get(id=id)

        obj1.delete()
        obj2.delete()

    except Exception as e:
        messages.error(request, "something went wrong")

    return redirect("/home/show-request")
    






    

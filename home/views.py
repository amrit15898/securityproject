from django.shortcuts import render, redirect
from .models import *
from .models import postions
import datetime
# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
@login_required
def post_appointment(request):

    try:
        gh_dh = User.objects.using("default").filter(position = "GH/DH")
        tech_dir = User.objects.using("default").filter(position = "Tech Director")
    
    except Exception as e:
        print(e)
    try:
        gh_dh = User.objects.using("new").filter(position = "GH/DH")
        tech_dir = User.objects.using("new").filter(position = "Tech Director")
    
    except Exception as e:
        print(e)

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
        try:
            obj.save(using="default")
        
        except Exception as e:
            print("ede ch nhi hoya")

        try:
            obj.save(using="new", force_insert=True)
        except Exception as e:
            print("chlya")


        return redirect("/home/seret")
      
    return render(request, "clearance.html", context)


@login_required
def show_request(request):

    try:
        user = request.user   
        context = {}
        try:
            if request.user.position == postions[3][1]:
   
                objs = Appointment.objects.using("default").filter(gh_dh__name=request.user,
                                                                   date__gte = datetime.datetime.now())
                
                print(objs)

    
            elif request.user.position == postions[2][1]:
                objs = Appointment.objects.using("default").filter(tech_dir__name = request.user)


            elif request.user.position == postions[0][1]:
                objs = Appointment.objects.using("new")
            elif request.user.position == postions[1][1]:
                objs = Appointment.objects.using("new") 
        except Exception as e:
            pass   
        try:
            if request.user.position == postions[3][1]:
   
                objs = Appointment.objects.using("new").filter(gh_dh__name=request.user,
                                                                   date__gte = datetime.datetime.now())

    
            elif request.user.position == postions[2][1]:
                objs = Appointment.objects.using("new").filter(tech_dir__name = request.user,
                                                                   date__gte = datetime.datetime.now())


            elif request.user.position == postions[0][1]:
                objs = Appointment.objects.using("new").filter(
                                                                   date__gte = datetime.datetime.now())
            elif request.user.position == postions[1][1]:
                objs = Appointment.objects.using("new").filter(                          date__gte = datetime.datetime.now()) 
        except Exception as e:
            pass  

            

        context["objs"] = objs

    
        if 'approved' in request.POST:
            value = request.POST.get("approved")
            obj1 = Appointment.objects.using("default").get(id=value)
            obj2 = Appointment.objects.using("new").get(id=value)
  
            position = request.user.position
       
            if (position == postions[3][1]):
                obj1.dh_gh_clr = "Approved"
                obj2.dh_gh_clr = "Approved"
                
                    
            if position == postions[2][1]:
                obj1.tech_dir_clr = "Approved"
                obj2.tech_dir_clr = "Approved"
                
            if position == postions[0][1]:
            
                obj1.dir_clr = "Approved"
                obj2.dir_clr = "Approved"
                
            if position == postions[1][1]:
                obj1.ass_dir_clr = "Approved"
                obj2.ass_dir_clr = "Approved"
                
            
            obj1.save()
            obj2.save()

         
        if 'napproved' in request.POST:
            value = request.POST.get("napproved")     
            obj1 = Appointment.objects.using("default").get(id=value)
            obj2 = Appointment.objects.using("new").get(id=value)
            position = request.user.position    
            if (position == postions[3][1]):
                print("gh called")
                obj1.dh_gh_clr = "Not Approved"
                obj2.dh_gh_clr = "Not Approved"
                
                    
            if position == postions[2][1]:
                print("gh called")
                obj1.tech_dir_clr = "Not Approved"
                obj2.tech_dir_clr = "Not Approved"
                
            if position == postions[0][1]:
                print("Associate director")
                obj1.dir_clr = "Not Approved"
                obj2.dir_clr = "Not Approved"
                
            if position == postions[1][1]:
                print("director")
                obj1.ass_dir_clr = "Not Approved"
                obj2.ass_dir_clr = "Not Approved"
                
            obj1.save()
            obj2.save()

                    

        if "forward" in request.POST:
            value = request.POST.get("forward")          
            obj1 = Appointment.objects.using("default").get(id=value)
            obj2 = Appointment.objects.using("new").get(id=value)         
            
            
            obj1.send_security = True
            obj2.send_security = True
            obj1.save()
            obj2.save()
            

   
        return render(request, "ghtechdir.html",context)

    except Exception as e:
        messages.warning(request, "something went wrong")
        return render(request, "ghtechdir.html",context)
        
    





@login_required
def employee_request(request):
    objs = Appointment.objects.filter(r_user = request.user)
    context = {"objs": objs}
    return render(request, "emprequest.html",context)


def show_full_request(request,id):
    try:    
        obj = Appointment.objects.using("default").get(id=id)
    except Exception as e:
        print(e)
    try:    
        obj = Appointment.objects.using("new").get(id=id)
    except Exception as e:
        print(e)

    context = {"obj": obj}
    return render(request, "fulldetail.html", context)


@login_required
def security_officer(request):
    try:
        objs = Appointment.objects.filter(send_security=True)
        context = {"objs": objs}
    except Exception as e:
        print(e)
    return render(request, "security.html", context)


@login_required
def full_security_detail(request,id):
    try:
        obj = Appointment.objects.get(id=id)
        context = {"obj": obj}
    except Exception as e:
        messages.warning(request, "something went wrong")
        return redirect("/home/security-panel")
    
    if "forward" in request.POST:
            value = request.POST.get("forward")          
            obj1 = Appointment.objects.using("default").get(id=value)
            obj2 = Appointment.objects.using("new").get(id=value)         
            
            
            obj1.send_security = True
            obj2.send_security = True
            obj1.save()
            obj2.save()
            

    return render(request, "fullsecurity.html", context)

@login_required
def cancel_request(request, id):
    try:
        obj1 = Appointment.objects.using("default").get(id=id)
        obj2 = Appointment.objects.using("new").get(id=id)

        obj1.delete()
        obj2.delete()

    except Exception as e:
        messages.error(request, "something went wrong")

    return redirect("/home/shsfsdfow-readfafquest")
    

@login_required   
def cleare_clearance_list(request):
    try:
        objs = Appointment.objects.using("default").filter(gh_dh__name= request.user, dir_clr="Approved")
    except Exception as e:
        pass
    try:
        objs = Appointment.objects.using("new").filter(gh_dh__name= request.user, dir_clr="Approved")
    except Exception as e:
        pass
    
    context = {"objs": objs}
    
    return render(request, "cleard.html", context)







    

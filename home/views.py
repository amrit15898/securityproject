from django.shortcuts import render, redirect
from .models import *
from .models import postions

# Create your views here.

from datetime import datetime, date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
todaydate = date.today()
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
            return redirect("/home/postapntent")
        
        if tdir == "SelectTD":
            messages.warning(request, "Please select tdir")
            return redirect("/home/postapntent")

        if department == "SelectDep":
            messages.warning(request, "Please the select the department")
            return redirect("/home/postapntent")

        final_gh_dh = User.objects.get(id=gh_dh)
        final_tech_dir = User.objects.get(id=tdir)
        d = date.split("T")

        pd = " ".join(d)
        print(pd)

       
        for obj in Appointment.objects.all():
            if str(obj.date.date()) == str(d[0]):
                print(obj.date)
                fmt = '%Y-%m-%d %H:%M'
                d1 = datetime.strptime(str(obj.date)[0:16], fmt)
                d2 = datetime.strptime(pd, fmt)

               
                minutes_diff = (d2- d1).total_seconds() / 60.0
                if minutes_diff<30:
                    print("please select the another time")
                    messages.warning(request, "please select another time")
                    return redirect("/home/postapntent")


        dep = Department.objects.get(id=department)
        obj = Appointment(gh_dh= final_gh_dh, tech_dir =final_tech_dir, description=description, department=dep, date=date)
        obj.r_user = request.user    
        obj.save()
        obj.save(using="new")
           
    return render(request, "clearance.html", context)


def update_appointment(request, id):
    try:
        obj = Appointment.objects.get(id=id)
        print(obj.description)
    except Exception as e:
        pass
    try:
        gh_dh = User.objects.using("default").filter(position="GH/DH")
        tech_dir = User.objects.using("default").filter(position="Tech Director")   
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
    context["obj"] = obj 
    context["ghid"] = obj.gh_dh.id
    context["td"] = obj.tech_dir.id
    context["depid"] = obj.department.id
    try:
        if request.method=="POST":
            gh_dh = request.POST.get("gh_dh")
            tdir = request.POST.get("tdir")
            description = request.POST.get("description")
            department = request.POST.get("department")
            final_gh_dh = User.objects.get(id=gh_dh)
            final_tech_dir = User.objects.get(id=tdir)
            dep = Department.objects.get(id=department)
            obj.gh_dh = final_gh_dh
            obj.tech_dir = final_tech_dir
            obj.description = description
            obj.department = dep
            try:
                obj.save()
            except Exception as e:
                pass             
            try:
                obj.save(using="new")        
            except Exception as e:
                pass
    except Exception as e:
        print(e)
    return render(request, "updateapp.html", context)


def show_request(request):
    print(request.user.name)
    print(request.user.position)
    user = request.user   
    context = {}
    try:
        try:
            if request.user.position == postions[3][1]:
                objs = Appointment.objects.using("default").filter(gh_dh__name=request.user,
                                                                   date__gte = datetime.now())       
            elif request.user.position == postions[2][1]:
                objs = Appointment.objects.using("default").filter(tech_dir__name = request.user)


            elif request.user.position == postions[0][1]:
                objs = Appointment.objects.filter(date__gte = datetime.now())
            elif request.user.position == postions[1][1]:
                objs = Appointment.objects.filter(date__gte = datetime.now()) 
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
                objs = Appointment.objects.using("new").filter(date__gte = datetime.datetime.now()) 
        except Exception as e:
            pass  

            

        context["objs"] = objs

    
        if 'approved' in request.POST:
            value = request.POST.get("approved")
            obj1 = Appointment.objects.using("default").get(id=value)
            obj2 = Appointment.objects.using("new").get(id=value)
  
            position = request.user.position
       
            if (position == postions[3][1]):
                try:
                    obj1.dh_gh_clr = "Approved"
                    obj2.dh_gh_clr = "Approved"
                except Exception as e:
                    pass
                
                    
            if position == postions[2][1]:
                try:
                    obj1.tech_dir_clr = "Approved"
                    obj2.tech_dir_clr = "Approved"
                except Exception as e:
                    pass
                
            if position == postions[0][1]:
            
                try:
                    obj1.dir_clr = "Approved"
                    obj2.dir_clr = "Approved"
                except Exception as e:
                    pass
                
            if position == postions[1][1]:
                try:
                    obj1.ass_dir_clr = "Approved"
                    obj2.ass_dir_clr = "Approved"
                except Exception as e:
                    pass
                
            
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
            

   
        return render(request, "ghdh2.html",context)

    except Exception as e:
        print(e)
        messages.warning(request, "something went wrong")
    return render(request, "ghdh2.html",context)
        
    





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


def forgot_password(request):
    if request.method == "POST":
        uidd = request.POST.get("id")
        user = User.objects.get(user_id=id)

        obj = ForgetMessageRequest(user_id = user)
        obj.save()
    
    return render(request, "forgotpass.html")







    

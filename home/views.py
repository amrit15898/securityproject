from django.shortcuts import render, redirect
from .models import *
from .models import postions
from django.utils import timezone
from datetime import timedelta
# Create your views here.
from datetime import datetime, date
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
todaydate = date.today().day
@login_required
def post_appointment(request):
    if request.user.position == "Employee":
        gh_dh = {}
        tech_dir = {}
        departments = {}
        context = {}
        try:
            gh_dh = User.objects.filter(position = "GH/DH")
            tech_dir = User.objects.filter(position = "Tech Director")
            departments = Department.objects.all()
            context["gh_dh"] = gh_dh
            context["tech_dir"] = tech_dir
            context["departments"] = departments   
        # try:
        #     gh_dh = User.objects.using("new").filter(position = "GH/DH")
        #     tech_dir = User.objects.using("new").filter(position = "Tech Director")
        
        # except Exception as e:
        #     print(e)   
            if request.method=="POST":
                organization = request.POST.get("organization")
                gh_dh = request.POST.get("gh_dh")
                tdir = request.POST.get("tdir")
                date = request.POST.get("date")  
                description = request.POST.get("description")
                items = request.POST.get("items")

                department = request.POST.get("department")
                dh_gh_clr = request.POST.get("dh_gh_clr")
                tech_dir_clr = request.POST.get("tech_dir_clr")
                ass_dir_clr = request.POST.get("ass_dir_clr")
                dir_clr = request.POST.get("dir_clr")
                
                if gh_dh == "SelectGH":
                    messages.warning(request, "Please select GH.")
                    return redirect("/home/postapntent")
                
                if tdir == "SelectTD":
                    messages.warning(request, "Please select Tech-Director.")
                    return redirect("/home/postapntent")

                if department == "SelectDep":
                    messages.warning(request, "Please select Department.")
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

                            messages.warning(request, "Please select another time slot, this slot is already booked.")
                            return redirect("/home/postapntent")

                dep = Department.objects.get(id=department)
                obj = Appointment(organization_name=organization, gh_dh= final_gh_dh, tech_dir =final_tech_dir, description=description,items =items,  department=dep, date=date)
                obj.r_user = request.user    
                obj.save()
                # obj.save(using="new")
            
        except Exception as e:
            print(e)
            
        return render(request, "clearance.html", context)
    
    return redirect('/')


def update_appointment(request, id):
    try:
        obj = Appointment.objects.get(id=id)
        
    except Exception as e:
        pass
    try:
        gh_dh = User.objects.using("default").filter(position="GH/DH")
        tech_dir = User.objects.using("default").filter(position="Tech Director")   
    except Exception as e:
        print(e)
    # try:
    #     gh_dh = User.objects.using("new").filter(position = "GH/DH")
    #     tech_dir = User.objects.using("new").filter(position = "Tech Director")
    
    # except Exception as e:
    #     print(e)
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
            # try:
            #     obj.save(using="new")        
            # except Exception as e:
            #     pass
    except Exception as e:
        print(e)
    return render(request, "updateapp.html", context)

@login_required
def show_request(request):
    if request.user.position == postions[3][1] or request.user.position == postions[2][1] or request.user.position == postions[0][1] or request.user.position == postions[1][1]:
        user = request.user   
        context = {}
        objs = {}
        try:
            try:
                if request.user.position == postions[3][1]:
                    objs = Appointment.objects.filter(gh_dh__name=request.user,
                                                                    date__gte = datetime.now()).exclude(dh_gh_clr = "Not Approved")       
                elif request.user.position == postions[2][1]:
                    objs = Appointment.objects.filter(tech_dir__name = request.user, date__gte = datetime.now(), dh_gh_clr = "Approved").exclude(tech_dir_clr = "Not approved")
                elif request.user.position == postions[0][1]:
                    objs = Appointment.objects.filter(date__gte = datetime.now())
                elif request.user.position == postions[1][1]:
                    objs = Appointment.objects.filter(date__gte = datetime.now(), tech_dir_clr ="Approved").exclude(ass_dir_clr  = "Not Approved")
            except Exception as e:
                pass  

            # try:
            #     if request.user.position == postions[3][1]:
    
            #         objs = Appointment.objects.using("new").filter(gh_dh__name=request.user,
            #                                                            date__gte = datetime.datetime.now())
            #     elif request.user.position == postions[2][1]:
            #         objs = Appointment.objects.using("new").filter(tech_dir__name = request.user,
            #                                                            date__gte = datetime.datetime.now())

            #     elif request.user.position == postions[0][1]:
            #         objs = Appointment.objects.using("new").filter(
            #                                                            date__gte = datetime.datetime.now())
            #     elif request.user.position == postions[1][1]:
            #         objs = Appointment.objects.using("new").filter(date__gte = datetime.datetime.now()) 
            # except Exception as e:
            #     pass         
            context["objs"] = objs
            if 'approved' in request.POST:
                value = request.POST.get("approved")
                obj1 = Appointment.objects.get(id=value)
                # obj2 = Appointment.objects.using("new").get(id=value)
                position = request.user.position
                if (position == postions[3][1]):
                    obj1.dh_gh_clr = "Approved"
                        # obj2.dh_gh_clr = "Approved"
                if position == postions[2][1]:
                    obj1.tech_dir_clr = "Approved"
                        # obj2.tech_dir_clr = "Approved"
                
                if position == postions[0][1]:
                        obj1.dir_clr = "Approved" 
                if position == postions[1][1]:
                    obj1.ass_dir_clr = "Approved"            
                obj1.save()
            
            if 'napproved' in request.POST:
                value = request.POST.get("napproved")     
                obj1 = Appointment.objects.get(id=value)
                # obj2 = Appointment.objects.using("new").get(id=value)
                position = request.user.position    
                if (position == postions[3][1]):
                    print("gh called")
                    obj1.dh_gh_clr = "Not Approved"
                    obj1.save()
                    # obj2.dh_gh_clr = "Not Approved"
                    # obj2.save()
                    return redirect(f"/home/cfhadf-regfsa/{value}")                    
                if position == postions[2][1]:
                    obj1.tech_dir_clr = "Not Approved"
                    obj1.save()
                    # obj2.tech_dir_clr = "Not Approved"
                    # obj1.save()
                    return redirect(f"/home/cfhadf-regfsa/{value}")               
                if position == postions[0][1]:
                    print("Associate director")
                    obj1.dir_clr = "Not Approved"
                    obj1.save()
                    # obj2.dir_clr = "Not Approved"
                    # obj2.save()
                    return redirect(f"/home/cfhadf-regfsa/{value}")         
                if position == postions[1][1]:
                    print("director")
                    obj1.ass_dir_clr = "Not Approved"
                    obj1.save()
                    # obj2.ass_dir_clr = "Not Approved"
                    # obj2.save()
                    return redirect("/home/shsfsdfow-readfafquest")
            if "forward" in request.POST:
                value = request.POST.get("forward")          
                obj1 = Appointment.objects.get(id=value)
                obj2 = Appointment.objects.using("new").get(id=value)                
                obj1.send_security = True
                obj1.save()
                # obj2.send_security = True
                # obj2.save()
            return render(request, "ghdh2.html",context)
        except Exception as e:
            messages.warning(request, "Something went wrong.")
        return render(request, "ghdh2.html",context)
    return redirect("/")
@login_required
def employee_request(request):
    objs = {}
    try:
        objs = Appointment.objects.filter(r_user = request.user)
        # objs = Appointment.objects.using("new").filter(r_user = request.user)
    except Exception as e:
        pass
    context = {"objs": objs}
    return render(request, "emprequest.html",context)

def show_full_request(request,id):
    try:    
        obj = Appointment.objects.get(id=id)
        # obj = Appointment.objects.using("new").get(id=id)
    except Exception as e:
        print(e)
    context = {"obj": obj}
    return render(request, "fulldetail.html", context)

@login_required
def security_officer(request):
    
    try:
        objs = Appointment.objects.filter(date__date__day = todaydate, dir_clr = "Approved" )
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
        messages.warning(request, "Something went wrong.")
        return redirect("/home/security-panel")
    if "forward" in request.POST:
            value = request.POST.get("forward")          
            obj1 = Appointment.objects.get(id=value)
            # obj2 = Appointment.objects.using("new").get(id=value)         
            obj1.send_security = True
            # obj2.send_security = True
            obj1.save()
            # obj2.save()
    return render(request, "fullsecurity.html", context)
@login_required
def cancel_request(request, id):
    try:
        obj1 = Appointment.objects.get(id=id)
        # obj2 = Appointment.objects.using("new").get(id=id)
        obj1.delete()
        # obj2.delete()
    except Exception as e:
        messages.error(request, "Something went wrong.")
    return redirect("/home/shsfsdfow-readfafquest")
    
@login_required   
def cleare_clearance_list(request):
    objs = {}
    try:
        objs = Appointment.objects.using("default").filter(gh_dh__name= request.user, dir_clr="Approved")
        # objs = Appointment.objects.using("new").filter(gh_dh__name= request.user, dir_clr="Approved")
    except Exception as e:
        pass
    context = {"objs": objs}  
    return render(request, "cleard.html", context)

def forgot_password(request):

    if request.method == "POST":
        uidd = request.POST.get("id")
        try:
            user = User.objects.get(employee_id=uidd)
        except Exception as e:
            messages.error(request, "ID does not match. Please check again.")
            return HttpResponseRedirect(request.path_info)
        obj = ForgetMessageRequest(employee_id = user)
        obj.save()
        # obj.save(using="new")
        messages.success(request, "Your request for password change has been sent.")
        return redirect("/")
    return render(request, "forgotpass.html")

@login_required
def reson_unopproved(request, id):
    try:
        obj = Appointment.objects.get(id=id)
        if request.method=="POST":
            reason = request.POST.get('reason')
            obj.reason_cancelation = reason
            obj.save()
            return redirect("/home/shsfsdfow-readfafquest")

    except Exception as e:
        pass
    return render(request, "cancelreason.html")



@login_required
def cancel_employee_request(request):
    objs = {}
    try:
        objs = Appointment.objects.filter(dh_gh_clr="Not Approved") | Appointment.objects.filter(tech_dir_clr="Not Approved") | Appointment.objects.filter(ass_dir_clr="Not Approved") | Appointment.objects.filter(dir_clr="Not Approved")
        # objs = Appointment.objects.using("new").filter(dh_gh_clr="Not Approved") | Appointment.objects.filter(tech_dir_clr="Not Approved") | Appointment.objects.filter(ass_dir_clr="Not Approved") | Appointment.objects.filter(dir_clr="Not Approved")
    except Exception as e:
        pass
    context = {}
    context["objs"] = objs 
    context["assdir"] = User.objects.filter(position = "Associate Director").first()
    context["dir"] = User.objects.filter(position = "Director").first()


    return render(request, "unapproved.html", context)


def show_cancel_reason(request,id):
    try:
        obj = Appointment.objects.get(id=id)
        # obj = Appointment.objects.using("new").get(id=id)
    except Exception as e:
        pass
    context = {"obj": obj}
    return render(request, "fullreason.html", context)
    

def show_employee_history(request, emp_id):
    try:
        objs = {}
        objs = Appointment.objects.filter(r_user__employee_id = emp_id)
        context = {"objs": objs}
    except Exception as e:
        print(e)

    return render(request, "emp_history.html", context)


def show_full_user_detail(request, id):
    user = User.objects.get(id=id)
    context ={"user":user}

    return render(request, "showfulluser.html",context)


def department_panel(request):
    appointments = {}
    if request.method == "POST":
        days = request.POST.get("days")
        today = timezone.now().date()
        if days == "last7days":
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)   
            appointments = Appointment.objects.filter(date__date__range=[start_date, end_date])& Appointment.objects.filter(department= request.user.department)
        elif  days == "today":
            appointments = Appointment.objects.filter(date__date = today)
        else:
            appointments = Appointment.objects.filter(department = request.user.department)

    context = {"appointments": appointments}
    return render(request, "departmentpanel.html", context)
    







    

from django.shortcuts import render, redirect
from .models import *
from .models import postions
# Create your views here.
def post_appointment(request):
    users = User.objects.all()
    departments = Department.objects.all()
    context = {}
    context["users"] = users 
    context["departments"] = departments 
    if request.method=="POST":
        user = request.POST.get("user")
    
        date = request.POST.get("date")
        description = request.POST.get("description")
        department = request.POST.get("department")
        dh_gh_clr = request.POST.get("dh_gh_clr")
        tech_dir_clr = request.POST.get("tech_dir_clr")
        ass_dir_clr = request.POST.get("ass_dir_clr")
        dir_clr = request.POST.get("dir_clr")
        userobj = User.objects.get(id=user)
        dep = Department.objects.get(id=department)
        obj = Appointment(user=userobj, description=description, department=dep, date=date)
        obj.r_user = request.user
        obj.save()
    return render(request, "clearance.html", context)


def show_request(request):
    user = request.user
    
    objs = Appointment.objects.filter(user=request.user)
    context = {"objs": objs}
    if 'approved' in request.POST:
        value = request.POST.get("approved")
      
        obj = Appointment.objects.get(id=value)
        position = request.user.position
       
        if (position == postions[3][1]):
            obj.dh_gh_clr = "Approved"
            
            
        elif position == postions[4][1]:
            obj.tech_dir_clr = "Approved"
            
        obj.save()   
      
    if "napproved" in request.POST:
        value = request.POST.get("napproved")
        obj = Appointment.objects.get(id=value)
       

        if request.user.position == postions[3][1]:
            obj.dh_gh_clr = "Not Approved"
            obj.save()
        elif request.user.position == postions[4][1]:
            obj.tech_dir_clr = "Not Approved"
            obj.save()      
    return render(request, "ghtechdir.html",context)


def director_page(request):  
    objs = Appointment.objects.all()
    context = {"objs": objs}
    return render(request, "director.html" ,context)



    

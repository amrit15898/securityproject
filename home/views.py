from django.shortcuts import render, redirect
from .models import *
from .models import postions
# Create your views here.
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

        final_gh_dh = User.objects.get(id=gh_dh)
        final_tech_dir = User.objects.get(id=tdir)


        dep = Department.objects.get(id=department)
        obj = Appointment(gh_dh= final_gh_dh, tech_dir =final_tech_dir, description=description, department=dep, date=date)
        obj.r_user = request.user
        # try:
        #     obj.save(using ="default")
        # except Exception as e:
        #     print(e)
        obj.save(using="new")
        obj.save(using="default")
      
    return render(request, "clearance.html", context)

def show_request(request):

    user = request.user   
    context = {}
  
    if request.user.position == postions[3][1]:
        print('error')
        objs = Appointment.objects.filter(gh_dh__name=request.user)

    
    elif request.user.position == postions[2][1]:
        objs = Appointment.objects.filter(tech_dir__name = request.user)


    elif request.user.position ==postions[0][1]:
        objs = Appointment.objects.all()
    elif request.user.position ==postions[1][1]:
        objs = Appointment.objects.all()    
    


    context["objs"] = objs
    if 'approved' in request.POST:
        value = request.POST.get("approved")
      
        obj = Appointment.objects.get(id=value)
        print(obj)
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
        print(obj)
        position = request.user.position
       
        if (position == postions[3][1]):
            obj.dh_gh_clr = "Not Approved"
            obj.save()
                    
        if position == postions[2][1]:
            obj.tech_dir_clr = "Not Approved"
            obj.save()
        if position == postions[0][1]:
            
            obj.dir_clr = "Not Approved"
            obj.save()
        if position == postions[1][1]:
            obj.ass_dir_clr = "Not Approved"
            obj.save()
            
   
      
   
    return render(request, "ghtechdir.html",context)




    

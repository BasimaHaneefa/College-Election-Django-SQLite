from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import *
from Student.models import *
from datetime import datetime
from django.utils.timezone import now
# Create your views here.
def homepage(request):
    admindata=tbl_admin.objects.get(id=request.session["aid"])
    return render(request,"Admin/Homepage.html",{'data':admindata})

def district(request):
    dis = tbl_district.objects.all()
    if request.method == "POST":
        tbl_district.objects.create(district_name=request.POST.get("txt_dis"))
        return redirect("Admin:district")
    else:
        return render(request,"Admin/District.html",{"data":dis})

def deldistrict(request,did):
    tbl_district.objects.get(id=did).delete()
    return redirect("Admin:district")   

def editdistrict(request,eid):
    disdata = tbl_district.objects.get(id=eid)
    if(request.method == "POST"):
        disdata.district_name=request.POST.get("txt_dis")
        disdata.save()
        return redirect("Admin:district")
    else:
        return render(request,"Admin/District.html",{"edit":disdata})

def place(request):
    disdata=tbl_district.objects.all()
    placedata=tbl_place.objects.all()
    if request.method == "POST":
        districtdata=tbl_district.objects.get(id=request.POST.get('sel_dis'))   
        tbl_place.objects.create(district=districtdata,place_name=request.POST.get('txt_place'))    
        return redirect("Admin:place")
    else:
        return render(request,"Admin/Place.html",{"dis":disdata,"data":placedata}) 

def delplace(request,pid):
    tbl_place.objects.get(id=pid).delete()
    return redirect("Admin:place")  

def editplace(request,eid):
    placedata = tbl_place.objects.get(id=eid)
    disdata=tbl_district.objects.all()
    if request.method == "POST":
        district=tbl_district.objects.get(id=request.POST.get("sel_dis"))
        placedata.place_name=request.POST.get("txt_place")
        placedata.district=district
        placedata.save()
        return redirect("Admin:place")
    else:
        return render(request,"Admin/Place.html",{"edit":placedata,"dis":disdata})        
    

def department(request):
    dis = tbl_department.objects.all()
    if request.method == "POST":
        tbl_department.objects.create(department_name=request.POST.get("txt_dep"))
        return redirect("Admin:department")
    else:
        return render(request,"Admin/Department.html",{"data":dis})

def deldepartment(request,did):
    tbl_department.objects.get(id=did).delete()
    return redirect("Admin:department")   

def editdepartment(request,eid):
    disdata = tbl_department.objects.get(id=eid)
    if(request.method == "POST"):
        disdata.department_name=request.POST.get("txt_dep")
        disdata.save()
        return redirect("Admin:department")
    else:
        return render(request,"Admin/Department.html",{"edit":disdata})


def collegeverification(request):
    verificationdata=tbl_newcollege.objects.filter(college_status=0)  
    return render(request,"Admin/CollegeVerification.html",{'data':verificationdata})

def accept(request,aid):
     verificationdata=tbl_newcollege.objects.get(id=aid)  
     verificationdata.college_status=1
     verificationdata.save()
     return redirect("Admin:collegeverification")

def reject(request,rid):
    verificationdata=tbl_newcollege.objects.get(id=rid) 
    verificationdata.college_status=2
    verificationdata.save()
    return redirect("Admin:collegeverification")    

def acceptedlist(request):
    verificationdata=tbl_newcollege.objects.filter(college_status=1)
    return render(request,"Admin/AcceptedCollege.html",{'data':verificationdata})
    
def rejectedlist(request):
    verificationdata=tbl_newcollege.objects.filter(college_status=2)
    return render(request,"Admin/RejectedCollege.html",{'data':verificationdata})

def course(request):
    departmentdata=tbl_department.objects.all()
    coursedata=tbl_course.objects.all()
    if request.method == "POST":
        departmentdata=tbl_department.objects.get(id=request.POST.get('sel_dep'))   
        tbl_course.objects.create(department=departmentdata,course_name=request.POST.get('txt_course'))    
        return redirect("Admin:course")
    else:
        return render(request,"Admin/Course.html",{"dep":departmentdata,"data":coursedata}) 

def delcourse(request,did):
    tbl_course.objects.get(id=did).delete()
    return redirect("Admin:course")     
             
def editcourse(request,eid):
    coursedata = tbl_course.objects.get(id=eid)
    departmentdata=tbl_department.objects.all()
    if request.method == "POST":
        department=tbl_department.objects.get(id=request.POST.get("sel_dep"))
        coursedata.course_name=request.POST.get("txt_course")
        coursedata.course_department=department
        coursedata.save()
        return redirect("Admin:course")
    else:
        return render(request,"Admin/Course.html",{"edit":coursedata,"dep":departmentdata})        

def position(request):
    positiondata=tbl_position.objects.all()
    if request.method == "POST":
        tbl_position.objects.create(position_name=request.POST.get('txt_position'))
        return redirect("Admin:position")
    else:
        return render(request,"Admin/Position.html",{"data":positiondata})     

def delposition(request,did):
    tbl_position.objects.get(id=did).delete()
    return redirect("Admin:position")              

def editposition(request,eid):
    positiondata=tbl_position.objects.get(id=eid)
    if request.method =="POST":
        positiondata.position_name=request.POST.get("txt_position")     
        positiondata.save()
        return redirect("Admin:position")
    else:
        return render(request,"Admin/Position.html",{"pdata":positiondata})    

def election(request):
    electiondata=tbl_election.objects.all()
    current_date = now().date()
    for election in electiondata:
        days_difference = (current_date - election.election_date).days
        election.days_difference = days_difference
    if request.method == "POST":
        tbl_election.objects.create(election_fordate=request.POST.get('txt_fordate'),election_details=request.POST.get('txt_details')) 
        return redirect("Admin:election")
    else:
        return render(request,"Admin/Election.html",{"data":electiondata,'current_date':current_date}) 
    
def electionstatus(request,eid):
    selelec=tbl_election.objects.get(id=eid)
    if selelec.election_status == '0':
        selelec.election_status=1
        selelec.save()
        return redirect("Admin:election")
    elif selelec.election_status == '1':
        selelec.election_status=2
        selelec.save()
        return redirect("Admin:election")
    elif selelec.election_status == '2':
        selelec.election_status=3
        selelec.save()
        return redirect("Admin:election")
    elif selelec.election_status == '3':
        selelec.election_status=4
        selelec.save()
        return redirect("Admin:election")
    else:
        return render(request,"Admin/Election.html")


def delelection(request,did):
    tbl_election.objects.get(id=did).delete()
    return redirect("Admin:election") 

def year(request):
    yeardata=tbl_year.objects.all()
    if request.method == "POST":
        tbl_year.objects.create(year_classyear=request.POST.get('txt_classyear'))
        return redirect("Admin:year")
    else:
        return render(request,"Admin/Year.html",{"data":yeardata})     

def delyear(request,did):
    tbl_year.objects.get(id=did).delete()
    return redirect("Admin:year")              

def edityear(request,eid):
    yeardata=tbl_year.objects.get(id=eid)
    if request.method =="POST":
        yeardata.year_classyear=request.POST.get("txt_classyear")     
        yeardata.save()
        return redirect("Admin:year")
    else:
        return render(request,"Admin/Year.html",{"ydata":yeardata})  

def reply(request,sid):
    studentcomplaint=tbl_complaint.objects.get(id=sid)
    if request.method=="POST":
        studentcomplaint.complaint_reply=request.POST.get('txt_reply')
        studentcomplaint.complaint_status=1
        studentcomplaint.save()
        return redirect("Admin:studentcomplaint")
    else:
        return render(request,"Admin/Reply.html")           

def studentcomplaint(request):
    studentcomplaint=tbl_complaint.objects.filter(complaint_status=0)
    repliedcomplaint=tbl_complaint.objects.filter(complaint_status=1)
    return render(request,"Admin/ViewStudentComplaint.html",{'data':studentcomplaint,'reply':repliedcomplaint})          

def studentfeedback(request):
    studentfeedback=tbl_feedback.objects.all()
    return render(request,"Admin/ViewStudentFeedback.html",{'data':studentfeedback})              
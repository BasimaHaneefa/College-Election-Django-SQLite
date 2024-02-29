from django.shortcuts import render,redirect
from Guest.models import *
from College.models import *
from Admin.models import *
from django.utils import timezone
from datetime import datetime
from django.db.models import F, Case, When, Value

# Create your views here.
def homepage(request):
    collegedata=tbl_newcollege.objects.get(id=request.session["cid"])
    return render(request,"College/Homepage.html",{'data':collegedata})

def myprofile(request):
    collegedatadata=tbl_newcollege.objects.get(id=request.session["cid"])
    return render(request,"College/MyProfile.html",{'data':collegedatadata})

def editprofile(request):
    collegedata=tbl_newcollege.objects.get(id=request.session["cid"])
    if request.method=="POST":
        collegedata.college_name=request.POST.get("txt_name")
        collegedata.college_contact=request.POST.get("txt_contact")
        collegedata.college_email=request.POST.get("txt_email")
        collegedata.college_address=request.POST.get("txt_address")
        collegedata.save()
        return render(request,"College/EditProfile.html",{'data':collegedata})    
    else:
        return render(request,"College/EditProfile.html",{'data':collegedata})   

def changepassword(request):
    if request.method=="POST":
       current=request.POST.get("txt_cpassword")
       new=request.POST.get("txt_npassword")
       confirm=request.POST.get("txt_password")
       collegecount=tbl_newcollege.objects.filter(id=request.session["cid"],college_password=current).count()
       if collegecount>0:
            college=tbl_newcollege.objects.get(id=request.session["cid"],college_password=current)
            if new==confirm:
                college.college_password=confirm
                college.save()
                return redirect("College:changepassword")
            else:
                return render(request,"College/ChangePassword.html")             
       else:
            return render(request,"College/ChangePassword.html")             
    else:
        return render(request,"College/ChangePassword.html")

def addteacher(request,eid):      
    coursedata=tbl_course.objects.all()
    college=tbl_newcollege.objects.get(id=request.session["cid"])
    teacherdata=tbl_teacher.objects.filter(teacher_college=college)
    departmentdata=tbl_department.objects.all()
    if request.method == 'POST':
        elec=tbl_election.objects.get(id=eid)
        newcollege=tbl_newcollege.objects.get(id=request.session["cid"])
        newcourse=tbl_course.objects.get(id=request.POST.get("sel_course"))
        newdep=tbl_department.objects.get(id=request.POST.get("sel_department"))
        tbl_teacher.objects.create(teacher_name=request.POST.get("txt_name"),
        teacher_address=request.POST.get("txt_address"),
        teacher_email=request.POST.get("txt_email"),
        teacher_contact=request.POST.get("txt_contact"),
        teacher_course=newcourse,
        teacher_college=newcollege,
        teacher_photo=request.FILES.get("file_photo"),
        teacher_password=request.POST.get("txt_pass"),
        election=elec)
        return redirect("College:addteacher", eid=eid)
    else:
        return render(request,"College/AddTeachers.html",{"data":teacherdata,"cou":coursedata,"dep":departmentdata})

def delteacher(request,did):
    tbl_teacher.objects.get(id=did).delete()
    return redirect("College:addteacher")   
    
def ajaxcourse(request):
    departmentdata=tbl_department.objects.get(id=request.GET.get("did"))
    coursedata=tbl_course.objects.filter(department=departmentdata)
    print(coursedata)
    return render(request,"College/AjaxCourse.html",{'course':coursedata}) 
  
def viewelection(request):
    electiondata=tbl_election.objects.all()
    return render(request, "College/ViewElection.html", {'data': electiondata})


def studentverification(request):
    clg=tbl_newcollege.objects.get(id=request.session["cid"])

    verificationdata=tbl_newstudent.objects.filter(student_ststus=0,student_college=clg)  
    return render(request,"College/StudentVerification.html",{'data':verificationdata})

def acceptstud(request,aid):
     verificationdata=tbl_newstudent.objects.get(id=aid)  
     verificationdata.student_ststus=1
     verificationdata.save()
     return redirect("College:studentverification")

def rejectstud(request,rid):
    verificationdata=tbl_newstudent.objects.get(id=rid) 
    verificationdata.student_ststus=2
    verificationdata.save()
    return redirect("College:studentverification")   

def acceptedlist(request):
    clg=tbl_newcollege.objects.get(id=request.session["cid"])
    verificationdata=tbl_newstudent.objects.filter(student_ststus=1,student_college=clg)
    return render(request,"College/AcceptedStudent.html",{'data':verificationdata})
    
def rejectedlist(request):
    clg=tbl_newcollege.objects.get(id=request.session["cid"])
    verificationdata=tbl_newstudent.objects.filter(student_ststus=2,student_college=clg)
    return render(request,"College/RejectedStudent.html",{'data':verificationdata})     


# def assignedteacher(request,eid):
#     assigndata=tbl_assignteacher.objects.filter(assign_election=eid)
#     return render(request, "College/AssignedTeacher.html",{"assign":assigndata})

# def teacherlist(request,eid):
#     request.session["eid"]=eid
#     collegedata=tbl_newcollege.objects.get(id=request.session["cid"])
#     teacher=tbl_teacher.objects.filter(teacher_college=collegedata)
#     assigned=tbl_assignteacher.objects.filter(assign_election=eid)
#     return render(request,"College/TeacherList.html",{'data':teacher,"assigned":assigned})  

# def AssignTeacher(request,tid):
#     eid=tbl_election.objects.get(id=request.session["eid"])
#     teacher=tbl_teacher.objects.get(id=tid)
#     tbl_assignteacher.objects.create(assign_teacher=teacher,assign_election=eid)
#     return redirect("College:viewelection")
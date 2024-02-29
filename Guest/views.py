from django.shortcuts import redirect, render
from Admin.models import *
from College.models import tbl_teacher
from Guest.models import *
# Create your views here.
def newcollege(request):
    disdata=tbl_district.objects.all()
    if request.method == 'POST':
        placedata=tbl_place.objects.get(id=request.POST.get("sel_place"))
        tbl_newcollege.objects.create(college_name=request.POST.get("txt_name"),
        college_address=request.POST.get("txt_address"),
        college_email=request.POST.get("txt_email"),
        college_contact=request.POST.get("txt_contact"),
        college_place=placedata,
        college_logo=request.FILES.get("file_logo"),
        college_proof=request.FILES.get("file_proof"),
        college_password=request.POST.get("txt_password")
        )
        return render(request,"Guest/NewCollege.html",{"dis":disdata})
    else:
        return render(request,"Guest/NewCollege.html",{"dis":disdata})

def ajaxplace(request):
    districtdata=tbl_district.objects.get(id=request.GET.get("did"))
    placedata=tbl_place.objects.filter(district=districtdata)
    print(placedata)
    return render(request,"Guest/AjaxPlace.html",{'place':placedata})  

def login(request):
    if request.method == 'POST':
        email=request.POST.get("txt_email")
        password=request.POST.get("txt_password") 
        count=tbl_newcollege.objects.filter(college_email=email,college_password=password,college_status=1).count()
        tcount=tbl_teacher.objects.filter(teacher_email=email,teacher_password=password).count()
        scount=tbl_newstudent.objects.filter(student_email=email,student_password=password,student_ststus=1).count()
        acount=tbl_admin.objects.filter(admin_email=email,admin_password=password).count()
        if count>0:
            collegedata=tbl_newcollege.objects.get(college_email=email,college_password=password,college_status=1)  
            request.session['cid']=collegedata.id   
            return redirect('College:homepage')
        elif tcount>0:
                teacherdata=tbl_teacher.objects.get(teacher_email=email,teacher_password=password)
                request.session['tid']=teacherdata.id
                return redirect('Teacher:homepage')
        elif scount>0:
                studentdata=tbl_newstudent.objects.get(student_email=email,student_password=password,student_ststus=1)
                request.session['sid']=studentdata.id
                return redirect('Student:homepage')   
        elif acount>0:
                admindata=tbl_admin.objects.get(admin_email=email,admin_password=password)
                request.session['aid']=admindata.id 
                return redirect('Admin:homepage')        
        else:
            msg="invalid login!!"
            return render(request,"Guest/Login.html",{"msg":msg})

    else:
        return render(request,"Guest/Login.html")
 
def newstudent(request):
    collegedata=tbl_newcollege.objects.filter(college_status=1)
    yeardata=tbl_year.objects.all()
    departmentdata=tbl_department.objects.all()
    if request.method == 'POST':
        newcollege=tbl_newcollege.objects.get(id=request.POST.get("sel_college"))
        newyear=tbl_year.objects.get(id=request.POST.get("sel_year"))
        newcourse=tbl_course.objects.get(id=request.POST.get("sel_course"))
        tbl_newstudent.objects.create(student_name=request.POST.get("txt_name"),
        student_address=request.POST.get("txt_address"),
        student_email=request.POST.get("txt_email"),
        student_contact=request.POST.get("txt_contact"),
        student_adno=request.POST.get("txt_adno"),
        student_college=newcollege,
        student_course=newcourse,
        student_year=newyear,
        student_photo=request.FILES.get("file_photo"),
        student_proof=request.FILES.get("file_proof"),
        student_password=request.POST.get("txt_password"),
        )
        return render(request,"Guest/NewStudents.html",{"dis":collegedata,"year":yeardata,"dep":departmentdata})
    else:
        return render(request,"Guest/NewStudents.html",{"dis":collegedata,"year":yeardata,"dep":departmentdata})
  
def ajaxcourse(request):
    departmentdata=tbl_department.objects.get(id=request.GET.get("did"))
    coursedata=tbl_course.objects.filter(department=departmentdata)
    print(coursedata)
    return render(request,"Guest/AjaxCourse.html",{'course':coursedata})   

def index(request):
    return render(request,"Guest/index.html")

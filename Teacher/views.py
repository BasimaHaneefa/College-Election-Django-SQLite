from collections import defaultdict
from django.db.models import Count
from django.shortcuts import get_object_or_404, render,redirect
from College.models import *
from Guest.models import *
from Student.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
# Create your views here.

def homepage(request):
    teacherdata=tbl_teacher.objects.get(id=request.session["tid"])
    return render(request,"Teacher/Homepage.html",{'data':teacherdata})

def myprofile(request):
    teacherdata=tbl_teacher.objects.get(id=request.session["tid"])
    return render(request,"Teacher/MyProfile.html",{'data':teacherdata})

def editprofile(request):
    teacherdata=tbl_teacher.objects.get(id=request.session["tid"])
    departmentdata=tbl_department.objects.all()
    collegedata=tbl_newcollege.objects.all()
    coursedata=tbl_course.objects.all()
    yeardata=tbl_year.objects.all()
    if request.method=="POST":
        department=tbl_department.objects.get(id=request.POST.get("sel_dep"))
        college=tbl_newcollege.objects.get(id=request.POST.get("sel_college"))
        course=tbl_course.objects.get(id=request.POST.get("sel_course"))
        year=tbl_year.objects.get(id=request.POST.get("sel_year"))
        teacher=tbl_teacher.objects.get(id=request.session["tid"])
        teacherdata.teacher_name=request.POST.get("txt_name")
        teacherdata.teacher_contact=request.POST.get("txt_contact")
        teacherdata.teacher_email=request.POST.get("txt_email")
        teacherdata.teacher_address=request.POST.get("txt_address")
        teacherdata.teacher_department=department
        teacherdata.teacher_course=course
        teacherdata.teacher_year=year
        teacherdata.teacher_college=college
        teacherdata.save()
        return render(request,"Teacher/Editprofile.html",{'data':teacherdata,'dep':departmentdata,'coll':collegedata,'cou':coursedata,'year':yeardata})    
    else:   
        return render(request,"Teacher/Editprofile.html",{'data':teacherdata,'dep':departmentdata,'coll':collegedata,'cou':coursedata,'year':yeardata})
        
def changepassword(request):
    if request.method=="POST":
       current=request.POST.get("txt_cpassword")
       new=request.POST.get("txt_npassword")
       confirm=request.POST.get("txt_password")
       teachercount=tbl_teacher.objects.filter(id=request.session["tid"],teacher_password=current).count()
       if teachercount>0:
            teacher=tbl_teacher.objects.get(id=request.session["tid"],teacher_password=current)
            if new==confirm:
                teacher.teacher_password=confirm
                teacher.save()
                return redirect("Teacher:changepassword")
            else:
                return render(request,"Teacher/ChangePasssword.html")             
       else:
            return render(request,"Teacher/ChangePasssword.html")             
    else:
        return render(request,"Teacher/ChangePasssword.html")


def classcandidate(request):
    teacher=tbl_teacher.objects.get(id=request.session["tid"])
    elec=teacher.election
    clg=teacher.teacher_college
    # assign=tbl_assignteacher.objects.get(id=eid)
    college=tbl_newcollege.objects.get(id=clg.id)
    electiondata=tbl_election.objects.get(id=elec.id)
    classcandidatedata=tbl_classcandidate.objects.filter(candidate_election=electiondata,candidate_student__student_college=college)
    return render(request,"Teacher/ClassCandidateApplication.html",{'data':classcandidatedata})    

def accept(request,aid):
    verificationdata=tbl_classcandidate.objects.get(id=aid)
    verificationdata.candidate_status=1
    verificationdata.save()
    return redirect("Teacher:classcandidate")

def reject(request,rid):
    verificationdata=tbl_classcandidate.objects.get(id=rid)
    verificationdata.candidate_status=2
    verificationdata.save()
    return redirect("Teacher:classcandidate")   

def clgdept(request):
    dept=tbl_department.objects.all()
    return render(request,"Teacher/clgdept.html",{'dept':dept})

def clgcourse(request,did):
    dept=tbl_department.objects.get(id=did)
    course=tbl_course.objects.filter(department=dept)
    return render(request,"Teacher/clgcourse.html",{'course':course})
def year(request,yid):
    request.session["coid"]=yid
    year=tbl_year.objects.all()
    return render(request,"Teacher/clgyear.html",{'year':year})
# def votedstudent(request):
#     voteddata=tbl_classpolling.objects.all()
#     return render(request,"Teacher/VotedStudentList.html",{'data':voteddata})

def classpolling(request, yid):
    teacher = tbl_teacher.objects.get(id=request.session["tid"])
    clg = teacher.teacher_college
    elec = teacher.election
    year = tbl_year.objects.get(id=yid)
    
    course = tbl_course.objects.get(id=request.session["coid"])
    winner = None
    try:
    
        winners = tbl_classcandidate.objects.filter(
        candidate_student__student_college=clg,
        candidate_election=elec,
        candidate_student__student_course=course,
        candidate_student__student_year=year,
        candidate_status=3
)
        for winner in winners:
            print(winner.candidate_student.student_name)
    except tbl_classcandidate.DoesNotExist:
        pass
    # Aggregate the total vote count for each candidate and include candidate ID
    polling_data = tbl_classpolling.objects.filter(
        polling_classcandidate__candidate_student__student_college=clg,
        polling_classcandidate__candidate_election=elec,
        polling_classcandidate__candidate_student__student_course=course,
        polling_classcandidate__candidate_student__student_year=year
    ).values(
        'polling_classcandidate__candidate_student__id',
        'polling_classcandidate__candidate_student__student_name'
    ).annotate(
        total_count=Count('polling_classcandidate__candidate_student')
    )

    return render(request, "Teacher/ClassPolling.html", {'polling': polling_data,'win':winner})

def winner(request,wid):
    polling=tbl_classpolling.objects.get(id=wid)
    can=polling.polling_classcandidate
    candidate=tbl_classcandidate.objects.get(id=can.id)
    candidate.candidate_status=3
    candidate.save()
    return redirect("Teacher:homepage")

def clgcandidate(request):
    teacher=tbl_teacher.objects.get(id=request.session["tid"])
    elec=teacher.election
    clg=teacher.teacher_college
    # assign=tbl_assignteacher.objects.get(id=eid)
    college=tbl_newcollege.objects.get(id=clg.id)
    electiondata=tbl_election.objects.get(id=elec.id)
    candidatedata=tbl_collegecandidate.objects.filter(election=electiondata,student__student_college=college)
    return render(request,"Teacher/CollegeCandidateApplication.html",{'data':candidatedata})    

def caccept(request,aid):
    verificationdata=tbl_collegecandidate.objects.get(id=aid)
    verificationdata.candidate_status=1
    verificationdata.save()
    return redirect("Teacher:clgcandidate")

def creject(request,rid):
    verificationdata=tbl_collegecandidate.objects.get(id=rid)
    verificationdata.candidate_status=2
    verificationdata.save()
    return redirect("Teacher:clgcandidate")   

def smark(request,sid):
    clgcandidatedata=tbl_collegecandidate.objects.all()
    markdata=tbl_semmark.objects.get(candidate=sid)
    if markdata.sem1 and markdata.sem2 and markdata.sem3  != '':
        sem1=float(markdata.sem1)
        sem2=float(markdata.sem2)
        sem3=float(markdata.sem3)
        return render(request,"Teacher/ViewMarks.html",{'data':markdata,'sem1':sem1,'sem2':sem2,'sem3':sem3})    
    elif markdata.sem1 and markdata.sem2 != '':
        sem1=float(markdata.sem1)
        sem2=float(markdata.sem2)
        return render(request,"Teacher/ViewMarks.html",{'data':markdata,'sem1':sem1,'sem2':sem2})    
    else:
        sem1=float(markdata.sem1)
        return render(request,"Teacher/ViewMarks.html",{'data':markdata,'sem1':sem1})   

def CollegeVotingResult(request):
    teacher = tbl_teacher.objects.get(id=request.session["tid"])
    election = teacher.election
    clg = teacher.teacher_college
    
    chairperson_winner = tbl_collegepolling.objects.filter(
    polling_student__student_college=clg,
    chairperson_candidate__election=election
    ).values('chairperson_candidate').annotate(
    vote_count=Count('chairperson_candidate')
    ).order_by('-vote_count').first()

# Similarly, query for other positions' winners
    vchairperson_winner = tbl_collegepolling.objects.filter(
    polling_student__student_college=clg,
    vchairperson_candidate__election=election
    ).values('vchairperson_candidate').annotate(
    vote_count=Count('vchairperson_candidate')
    ).order_by('-vote_count').first()

    general_winner = tbl_collegepolling.objects.filter(
    polling_student__student_college=clg,
    general_candidate__election=election
    ).values('general_candidate').annotate(
    vote_count=Count('general_candidate')
    ).order_by('-vote_count').first()

    arts_winner = tbl_collegepolling.objects.filter(
    polling_student__student_college=clg,
    arts_candidate__election=election
    ).values('arts_candidate').annotate(
    vote_count=Count('arts_candidate')
    ).order_by('-vote_count').first()

    first_winner = tbl_collegepolling.objects.filter(
    polling_student__student_college=clg,
    first_candidate__election=election
    ).values('first_candidate').annotate(
    vote_count=Count('first_candidate')
    ).order_by('-vote_count').first()

    sec_winner = tbl_collegepolling.objects.filter(
    polling_student__student_college=clg,
    sec_candidate__election=election
    ).values('sec_candidate').annotate(
    vote_count=Count('sec_candidate')
    ).order_by('-vote_count').first()

    third_winner = tbl_collegepolling.objects.filter(
    polling_student__student_college=clg,
    third_candidate__election=election
    ).values('third_candidate').annotate(
    vote_count=Count('third_candidate')
    ).order_by('-vote_count').first()

    lady_winner = tbl_collegepolling.objects.filter(
    polling_student__student_college=clg,
    lady_candidate__election=election
    ).values('lady_candidate').annotate(
    vote_count=Count('lady_candidate')
    ).order_by('-vote_count').first()

    editor_winner = tbl_collegepolling.objects.filter(
    polling_student__student_college=clg,
    editor_candidate__election=election
    ).values('editor_candidate').annotate(
    vote_count=Count('editor_candidate')
    ).order_by('-vote_count').first()

    union_winner = tbl_collegepolling.objects.filter(
    polling_student__student_college=clg,
    union_candidate__election=election
    ).values('union_candidate').annotate(
    vote_count=Count('union_candidate')
    ).order_by('-vote_count').first()

# Extracting only the IDs
    chairperson_winner_id = chairperson_winner['chairperson_candidate'] if chairperson_winner else None
    vchairperson_winner_id = vchairperson_winner['vchairperson_candidate'] if vchairperson_winner else None
    general_winner_id = general_winner['general_candidate'] if general_winner else None
    arts_winner_id = arts_winner['arts_candidate'] if arts_winner else None
    first_winner_id = first_winner['first_candidate'] if first_winner else None
    sec_winner_id = sec_winner['sec_candidate'] if sec_winner else None
    third_winner_id = third_winner['third_candidate'] if third_winner else None
    lady_winner_id = lady_winner['lady_candidate'] if lady_winner else None
    editor_winner_id = editor_winner['editor_candidate'] if editor_winner else None
    union_winner_id = union_winner['union_candidate'] if union_winner else None

    chairperson_winner_candidate = tbl_collegecandidate.objects.get(id=chairperson_winner_id)
    vchairperson_winner_candidate = tbl_collegecandidate.objects.get(id=vchairperson_winner_id)
    general_winner_candidate = tbl_collegecandidate.objects.get(id=general_winner_id)
    arts_winner_candidate = tbl_collegecandidate.objects.get(id=arts_winner_id)
    first_winner_candidate = tbl_collegecandidate.objects.get(id=first_winner_id)
    sec_winner_candidate = tbl_collegecandidate.objects.get(id=sec_winner_id)
    third_winner_candidate = tbl_collegecandidate.objects.get(id=third_winner_id)
    editor_winner_candidate = tbl_collegecandidate.objects.get(id=editor_winner_id)
    lady_winner_candidate = tbl_collegecandidate.objects.get(id=lady_winner_id)
    union_winner_candidate = tbl_collegecandidate.objects.get(id=union_winner_id)

# Retrieve student names for all winners
    chairperson_winner_name = chairperson_winner_candidate.student.student_name if chairperson_winner_candidate else None
    vchairperson_winner_name = vchairperson_winner_candidate.student.student_name if vchairperson_winner_candidate else None
    general_winner_name = general_winner_candidate.student.student_name if general_winner_candidate else None
    arts_winner_name = arts_winner_candidate.student.student_name if arts_winner_candidate else None
    first_winner_name = first_winner_candidate.student.student_name if first_winner_candidate else None
    sec_winner_name = sec_winner_candidate.student.student_name if sec_winner_candidate else None
    third_winner_name = third_winner_candidate.student.student_name if third_winner_candidate else None
    editor_winner_name = editor_winner_candidate.student.student_name if editor_winner_candidate else None
    lady_winner_name = lady_winner_candidate.student.student_name if lady_winner_candidate else None
    union_winner_name = union_winner_candidate.student.student_name if union_winner_candidate else None


    return render(request, "Teacher/CollegeElectionResult.html", {
    'chairperson_winner_name': chairperson_winner_name,
    'vchairperson_winner_name': vchairperson_winner_name,
    'general_winner_name': general_winner_name,
    'arts_winner_name': arts_winner_name,
    'first_winner_name': first_winner_name,
    'sec_winner_name': sec_winner_name,
    'third_winner_name': third_winner_name,
    'editor_winner_name': editor_winner_name,
    'lady_winner_name': lady_winner_name,
    'union_winner_name': union_winner_name,
})
from datetime import datetime
from django.utils.timezone import now
from django.shortcuts import render,redirect
from College.models import *
from Guest.models import *
from Admin.models import *
from Student.models import *
from django.db.models import Count
# Create your views here.

def homepage(request):
    studentdata=tbl_newstudent.objects.get(id=request.session["sid"])
    # Assuming you have identified the current election
    
    return render(request, 'Student/Homepage.html', {'data':studentdata})



def myprofile(request):
    studentdata=tbl_newstudent.objects.get(id=request.session["sid"])
    return render(request,"Student/MyProfile.html",{'data':studentdata})

def editprofile(request):
    studentdata=tbl_newstudent.objects.get(id=request.session["sid"])
    yeardata=tbl_year.objects.all()
    if request.method=="POST":
        year=tbl_year.objects.get(id=request.POST.get("sel_year"))
        studentdata.student_name=request.POST.get("txt_name")
        studentdata.student_contact=request.POST.get("txt_contact")
        studentdata.student_email=request.POST.get("txt_email")
        studentdata.student_address=request.POST.get("txt_address")
        studentdata.student_year=year
        studentdata.save()
        return render(request,"Student/EditProfile.html",{'data':studentdata,'year':yeardata})    
    else:
        return render(request,"Student/EditProfile.html",{'data':studentdata,'year':yeardata})   

def changepassword(request):
    if request.method=="POST":
       current=request.POST.get("txt_cpassword")
       new=request.POST.get("txt_npassword")
       confirm=request.POST.get("txt_password")
       studentcount=tbl_newstudent.objects.filter(id=request.session["sid"],student_password=current).count()
       if studentcount>0:
            student=tbl_newstudent.objects.get(id=request.session["sid"],student_password=current)
            if new==confirm:
                student.student_password=confirm
                student.save()
                return redirect("Student:changepassword")
            else:
                return render(request,"Student/ChangePassword.html")             
       else:
            return render(request,"Student/ChangePassword.html")             
    else:
        return render(request,"Student/ChangePassword.html")

def complaint(request):
    studentdata=tbl_newstudent.objects.get(id=request.session["sid"])
    complaintdata=tbl_complaint.objects.filter(student=studentdata)
    if request.method=="POST":
        tbl_complaint.objects.create(
            complaint_title=request.POST.get("txt_name"),
            complaint_content=request.POST.get("txt_content"),
            student=studentdata)
        return render(request,"Student/Complaint.html",{'data':complaintdata})
    else:
        return render(request,"Student/Complaint.html",{'data':complaintdata})     

def delcomplaint(request,sid):
    tbl_complaint.objects.get(id=sid).delete()
    return redirect("Student:complaint")    

def feedback(request):
    studentdata=tbl_newstudent.objects.get(id=request.session["sid"])
    feedbackdata=tbl_feedback.objects.filter(student=studentdata)
    if request.method == 'POST':
        tbl_feedback.objects.create(
            feedback_content=request.POST.get("txt_feedback"),
            student=studentdata)
        return render(request,"Student/Feedback.html",{'data':feedbackdata})
    else:
        return render(request,"Student/Feedback.html",{'data':feedbackdata})

def delfeedback(request,sid):
    tbl_feedback.objects.get(id=sid).delete()
    return redirect("Student:feedback")        

def viewelection(request):
    
    electiondata = tbl_election.objects.all()
    studentdata=tbl_newstudent.objects.get(id=request.session["sid"])
    current_election = tbl_election.objects.filter(election_date__lte=datetime.now()).latest('election_date')
    candidate=tbl_classcandidate.objects.get(candidate_election=current_election.id,candidate_student=studentdata)
    current_date = now().date()
    for election in electiondata:
        days_difference = (current_date - election.election_date).days
        election.days_difference = days_difference
    return render(request, "Student/ViewElection.html", {'data': electiondata,'current_date':current_date,'cand':candidate})

def viewcandidate(request,eid):
    studentdata=tbl_newstudent.objects.get(id=request.session["sid"])
    electiondata=tbl_election.objects.get(id=eid)
    if request.method == 'POST':
        tbl_classcandidate.objects.create(
            candidate_gender=request.POST.get("radio"),
            candidate_election=electiondata,
            candidate_student=studentdata)
        return redirect("Student:viewmyapplication")
    else:
        return render(request,"Student/ClassCandidate.html",{"data":studentdata})  

def viewmyapplication(request):
    studentdata=tbl_newstudent.objects.get(id=request.session["sid"])
    candidate=tbl_classcandidate.objects.filter(candidate_student=studentdata)
    application=tbl_collegecandidate.objects.filter(student=studentdata)
    return render(request,"Student/ViewMyApplication.html",{'data':candidate,'app':application})    

def candidate(request,eid):
    election=tbl_election.objects.get(id=eid)
    student=tbl_newstudent.objects.get(id=request.session["sid"])
    candidatedata=tbl_classcandidate.objects.filter(candidate_student__student_course=student.student_course,candidate_student__student_college=student.student_college,candidate_student__student_year=student.student_year,candidate_status=1,candidate_election=election)
    return render(request,"Student/ClassVoting.html",{'data':candidatedata})

def vote(request,sid):
    candidate=tbl_classcandidate.objects.get(id=sid)
    student=tbl_newstudent.objects.get(id=request.session["sid"])
    electiondata=tbl_election.objects.get(id=candidate.candidate_election.id)
    tbl_classpolling.objects.create(polling_classcandidate=candidate,polling_student=student)
    return redirect("Student:homepage")

def classresult(request,eid):
    current_election = tbl_election.objects.get(id=eid)
    # Retrieve the student
    student = tbl_newstudent.objects.get(id=request.session["sid"])

    # Retrieve class candidates for the current election in the same college, course, and year
    class_candidates = tbl_classcandidate.objects.filter(
        candidate_election=current_election,
        candidate_student__student_college=student.student_college,
        candidate_student__student_course=student.student_course,
        candidate_student__student_year=student.student_year
    )

    # Retrieve polling results for each candidate
    results = []
    for candidate in class_candidates:
        votes = tbl_classpolling.objects.filter(polling_classcandidate=candidate).count()
        results.append({'candidate': candidate, 'votes': votes})

    # Identify the winner
    if results:
        winner = max(results, key=lambda x: x['votes'])
        winner_name = winner['candidate'].candidate_student.student_name
        total_votes = winner['votes']
    else:
        winner_name = "No winner"
        total_votes = 0

    return render(request,"Student/ClassResult.html",{'winner_name': winner_name, 'total_votes': total_votes})
   
def CollegeCandidate(request,eid):
    position=tbl_position.objects.all()
    student=tbl_newstudent.objects.get(id=request.session["sid"])
    electiondata=tbl_election.objects.get(id=eid)
    if request.method=="POST":
        post=tbl_position.objects.get(id=request.POST.get("Position"))
        tbl_collegecandidate.objects.create(student=student,
                                            election=electiondata,
                                            position=post)
        return redirect("Student:viewmyapplication")
    else:
        return render(request,"Student/CollegeCandidate.html",{'post':position,'data':student})
    
def Semmark(request,eid):
    candidate=tbl_collegecandidate.objects.get(id=eid)
    mark=tbl_semmark.objects.filter(candidate=candidate)
    if request.method=="POST":
        
        tbl_semmark.objects.create(sem1=request.POST.get("sem1"),
                               sem2=request.POST.get("sem2"),
                               sem3=request.POST.get("sem3"),
                               candidate=candidate)
        return redirect("Student:viewmyapplication")
    else:
        return render(request,"Student/SemMark.html",{'mark':mark})
    
def collegevoting(request,eid):
    student=tbl_newstudent.objects.get(id=request.session["sid"])
    clg=student.student_college
    election=tbl_election.objects.get(id=eid)
    chairperson_position = tbl_position.objects.get(position_name="Chairperson")
    vchairperson_position = tbl_position.objects.get(position_name="Vice-Chairperson")
    general_position = tbl_position.objects.get(position_name="General Secretary")
    arts_position = tbl_position.objects.get(position_name="Arts Club Secretary")
    first_position = tbl_position.objects.get(position_name="1st year Representative")
    sec_position = tbl_position.objects.get(position_name="2nd year Representative")
    third_position = tbl_position.objects.get(position_name="3rd year Representative")
    editor_position = tbl_position.objects.get(position_name="Magazine Editor")
    lady_position = tbl_position.objects.get(position_name="Lady Representative")
    union_position = tbl_position.objects.get(position_name="Councillor  to the University Union")
    chairperson_candidates = tbl_collegecandidate.objects.filter(position=chairperson_position.id,student__student_college=clg,candidate_status=1,election=election)
    vchairperson_candidates = tbl_collegecandidate.objects.filter(position=vchairperson_position.id,student__student_college=clg,candidate_status=1,election=election)
    general_candidates = tbl_collegecandidate.objects.filter(position=general_position.id,student__student_college=clg,candidate_status=1,election=election)
    arts_candidates = tbl_collegecandidate.objects.filter(position=arts_position.id,student__student_college=clg,candidate_status=1,election=election)
    frst_candidates = tbl_collegecandidate.objects.filter(position=first_position.id,student__student_college=clg,candidate_status=1,election=election)
    sec_candidates = tbl_collegecandidate.objects.filter(position=sec_position.id,student__student_college=clg,candidate_status=1,election=election)
    third_candidates = tbl_collegecandidate.objects.filter(position=third_position.id,student__student_college=clg,candidate_status=1,election=election)
    editor_candidates = tbl_collegecandidate.objects.filter(position=editor_position.id,student__student_college=clg,candidate_status=1,election=election)
    lady_candidates = tbl_collegecandidate.objects.filter(position=lady_position.id,student__student_college=clg,candidate_status=1,election=election)
    union_candidates = tbl_collegecandidate.objects.filter(position=union_position.id,student__student_college=clg,candidate_status=1,election=election)
    if request.method == "POST":
        chairperson_candidate = tbl_collegecandidate.objects.get(id=request.POST.get("ChairPerson"))
        print(chairperson_candidate.id)
        vchairperson_candidate = tbl_collegecandidate.objects.get(id=request.POST.get("VChairPerson"))
        general_candidate = tbl_collegecandidate.objects.get(id=request.POST.get("GeneralSecretary"))
        arts_candidate = tbl_collegecandidate.objects.get(id=request.POST.get("ArtsClubSecretary"))
        first_candidate = tbl_collegecandidate.objects.get(id=request.POST.get("1styearepresentative"))
        sec_candidate = tbl_collegecandidate.objects.get(id=request.POST.get("2ndyearepresentative"))
        third_candidate = tbl_collegecandidate.objects.get(id=request.POST.get("3rdyearepresentative"))
        editor_candidate = tbl_collegecandidate.objects.get(id=request.POST.get("MagazineEditor"))
        lady_candidate = tbl_collegecandidate.objects.get(id=request.POST.get("LadyRepresentative"))
        union_candidate = tbl_collegecandidate.objects.get(id=request.POST.get("CouncillortotheUniversityUnion"))
   
        tbl_collegepolling.objects.create(chairperson_candidate=chairperson_candidate,
                                      vchairperson_candidate=vchairperson_candidate,
                                      general_candidate=general_candidate,
                                      arts_candidate=arts_candidate,
                                      first_candidate=first_candidate,
                                      sec_candidate=sec_candidate,
                                      third_candidate=third_candidate,
                                      lady_candidate=lady_candidate,
                                      editor_candidate=editor_candidate,
                                      union_candidate=union_candidate,
                                      polling_student=student)
        return redirect("Student:homepage")
    else:
        return render(request,"Student/CollegeVoting.html",{'chairperson':chairperson_candidates,'vc':vchairperson_candidates,'gen':general_candidates,'arts':arts_candidates,'fst':frst_candidates,'sec':sec_candidates,'td':third_candidates,'lady':lady_candidates,'edit':editor_candidates,'union':union_candidates})

def CollegeVotingResult(request,eid):
    student=tbl_newstudent.objects.get(id=request.session["sid"])
    clg = student.student_college
    elec=tbl_election.objects.get(id=eid)
    election = elec.id
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


    return render(request, "Student/CollegeElectionResult.html", {
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
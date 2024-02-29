from django.urls import path,include
from Student import views
app_name="Student"

urlpatterns = [
    path("homepage",views.homepage,name="homepage"),

    path("myprofile",views.myprofile,name="myprofile"),
    path("editprofile/",views.editprofile,name="editprofile"),
    path("changepassword/",views.changepassword,name="changepassword"),

    path("complaint/",views.complaint,name="complaint"),
    path('delcomplaint/<int:sid>',views.delcomplaint,name="delcomplaint"),

    path("feedback/",views.feedback,name="feedback"),
    path("delfeedback/<int:sid>",views.delfeedback,name="delfeedback"),

    path("viewelection/",views.viewelection,name="viewelection"),

    path("viewcandidate/<int:eid>",views.viewcandidate,name="viewcandidate"),

    path("viewmyapplication/",views.viewmyapplication,name="viewmyapplication"),

    path("candidate/<int:eid>",views.candidate,name="candidate"),
    path("vote/<int:sid>",views.vote,name="vote"),
    path("classresult/<int:eid>",views.classresult,name="classresult"),

    path("CollegeCandidate/<int:eid>",views.CollegeCandidate,name="CollegeCandidate"),
    path("Semmark/<int:eid>",views.Semmark,name="Semmark"),

    path("collegevoting/<int:eid>",views.collegevoting,name="collegevoting"),

    path("CollegeVotingResult/<int:eid>",views.CollegeVotingResult,name="CollegeVotingResult"),
]
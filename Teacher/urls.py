from django.urls import path,include
from Teacher import views
app_name="Teacher"

urlpatterns = [
    path("homepage",views.homepage,name="homepage"),
    path("myprofile",views.myprofile,name="myprofile"),
    path("editprofile",views.editprofile,name="editprofile"),
    path("changepassword",views.changepassword,name="changepassword"),

    
    path("classcandidate/",views.classcandidate,name="classcandidate"),
    path("accept/<int:aid>",views.accept,name="accept"),
    path("reject/<int:rid>",views.reject,name="reject"),

    path("clgdept/",views.clgdept,name="clgdept"),
    path("clgcourse/<int:did>",views.clgcourse,name="clgcourse"),
    path("year/<int:yid>",views.year,name="year"),

    # path("votedstudent/",views.votedstudent,name="votedstudent"),

    path('classpolling/<int:yid>',views.classpolling,name="classpolling"),
    path('winner/<int:wid>', views.winner, name='winner'),

    path("clgcandidate/",views.clgcandidate,name="clgcandidate"),
    path("caccept/<int:aid>",views.caccept,name="caccept"),
    path("creject/<int:rid>",views.creject,name="creject"),
    path("smark/<int:sid>",views.smark,name="smark"),
    path("CollegeVotingResult/",views.CollegeVotingResult,name="CollegeVotingResult"),
]
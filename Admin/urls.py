from django.urls import path,include
from Admin import views
app_name="Admin"

urlpatterns = [
    path('homepage/',views.homepage,name="homepage"),
    path("district/",views.district,name="district"),
    path("deldistrict/<int:did>",views.deldistrict,name="deldistrict"),
    path("editdistrict/<int:eid>",views.editdistrict,name="editdistrict"),

    path("place/",views.place,name="place"),
    path("delplace/<int:pid>",views.delplace,name="delplace"),
    path("editplace/<int:eid>",views.editplace,name="editplace"),

    path("department/",views.department,name="department"),
    path("deldepartment/<int:did>",views.deldepartment,name="deldepartment"),
    path("editdepartment/<int:eid>",views.editdepartment,name="editdepartment"),

    path("collegeverification/",views.collegeverification,name="collegeverification"),
    path("accept/<int:aid>",views.accept,name="accept"),
    path("reject/<int:rid>",views.reject,name="reject"),

    path("acceptedlist/",views.acceptedlist,name="acceptedlist"),
    path("rejectedlist/",views.rejectedlist,name="rejectedlist"),

    path("course/",views.course,name="course"),
    path("delcourse/<int:did>",views.delcourse,name="delcourse"),
    path("editcourse/<int:eid>",views.editcourse,name="editcourse"),

    path("position/",views.position,name="position"),
    path("delposition/<int:did>",views.delposition,name="delposition"),
    path("editposition/<int:eid>",views.editposition,name="editposition"),

    path("election/",views.election,name="election"),
    path("electionstatus/<int:eid>",views.electionstatus,name="electionstatus"),
    path("delelection/<int:did>",views.delelection,name="delelection"),

    path("year/",views.year,name="year"),
    path("delyear/<int:did>",views.delyear,name="delyear"),
    path("edityear/<int:eid>",views.edityear,name="edityear"),
    
    path('studentcomplaint/',views.studentcomplaint,name="studentcomplaint"),
    path('reply/<int:sid>',views.reply,name="reply"),

    path('reply/',views.reply,name="reply"),

    path('studentfeedback/',views.studentfeedback,name="studentfeedback"),
]
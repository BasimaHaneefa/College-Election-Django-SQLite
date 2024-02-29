from django.urls import path,include
from College import views
app_name="College"

urlpatterns = [
    path("homepage/",views.homepage,name="homepage"),

    path("myprofile/",views.myprofile,name="myprofile"),
    path("editprofile/",views.editprofile,name="editprofile"),
    path("changepassword/",views.changepassword,name="changepassword"),

    path("addteacher/<int:eid>",views.addteacher,name="addteacher"),
    path("delteacher/<int:did>",views.delteacher,name="delteacher"),
    path("ajaxcourse/",views.ajaxcourse,name="ajaxcourse"),

    path("viewelection/",views.viewelection,name="viewelection"),
    # path("assignedteacher/<int:eid>",views.assignedteacher,name="assignedteacher"),

    # path("teacherlist/<int:eid>",views.teacherlist,name="teacherlist"),
    # path('assign_teacher/<int:tid>', views.AssignTeacher, name='assignteacher'),

    path("studentverification/",views.studentverification,name="studentverification"),
    path("accept/<int:aid>",views.acceptstud,name="acceptstud"),
    path("reject/<int:rid>",views.rejectstud,name="rejectstud"),
    path("acceptedlist/",views.acceptedlist,name="acceptedlist"),
    path("rejectedlist/",views.rejectedlist,name="rejectedlist"),

]
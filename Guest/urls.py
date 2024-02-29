from django.urls import path,include
from Guest import views
app_name="Guest"

urlpatterns = [
    path("newcollege/",views.newcollege,name="newcollege"),
    path("ajaxplace/",views.ajaxplace,name="ajaxplace"),

    path("login/",views.login,name="login"),

    path("newstudent/",views.newstudent,name="newstudent"),
    path("ajaxcourse/",views.ajaxcourse,name="ajaxcourse"),

    path("index/",views.index,name="index"),
]
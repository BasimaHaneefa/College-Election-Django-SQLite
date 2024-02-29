from django.db import models

# Create your models here.
from django.db import models
from Admin.models import *

# Create your models here.
class tbl_district(models.Model):
    district_name=models.CharField(max_length=50)

class tbl_place(models.Model):
    place_name=models.CharField(max_length=50)
    district=models.ForeignKey(tbl_district,on_delete=models.CASCADE)

class tbl_department(models.Model):
    department_name=models.CharField(max_length=50)   

class tbl_course(models.Model):
    department=models.ForeignKey(tbl_department,on_delete=models.CASCADE)
    course_name=models.CharField(max_length=50)

class tbl_position(models.Model):
    position_name=models.CharField(max_length=50)

class tbl_election(models.Model):
    election_date=models.DateField(auto_now_add=True)
    election_fordate=models.DateField()
    election_details=models.CharField(max_length=500) 
    election_status=models.CharField(max_length=10,default=0)

class tbl_year(models.Model):
    year_classyear=models.CharField(max_length=10)  

class tbl_admin(models.Model):
    admin_name=models.CharField(max_length=10)
    admin_email=models.EmailField(max_length=20)
    admin_password=models.CharField(max_length=10,unique=True)      

        
         
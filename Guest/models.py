from django.db import models
from Admin.models import *
# Create your models here.
class tbl_newcollege(models.Model):
    college_name=models.CharField(max_length=50)
    college_address=models.CharField(max_length=100)
    college_email=models.EmailField(unique="true")
    college_contact=models.CharField(max_length=50)
    college_place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
    college_logo=models.FileField(upload_to='CollegeLogo/')
    college_proof=models.FileField(upload_to='CollegeProof/')
    college_password=models.CharField(max_length=50,unique="true")
    college_status=models.CharField(max_length=20,default=0)

class tbl_newstudent(models.Model):
    student_name=models.CharField(max_length=50)
    student_address=models.CharField(max_length=100)
    student_email=models.EmailField(unique="true")
    student_contact=models.CharField(max_length=50)
    student_adno=models.CharField(max_length=50)
    student_college=models.ForeignKey(tbl_newcollege,on_delete=models.CASCADE)
    student_course=models.ForeignKey(tbl_course,on_delete=models.CASCADE)
    student_year=models.ForeignKey(tbl_year,on_delete=models.CASCADE)
    student_photo=models.FileField(upload_to='StudentPhoto/')
    student_proof=models.FileField(upload_to='StudentProof/')
    student_password=models.CharField(max_length=50,unique="true")
    student_ststus=models.CharField(max_length=20,default=0)
from django.db import models
from Admin.models import *
from Guest.models import tbl_newcollege
# Create your models here.
class tbl_teacher(models.Model):
    teacher_name=models.CharField(max_length=50)
    teacher_address=models.CharField(max_length=500)
    teacher_email=models.EmailField(max_length=30,unique=True)
    teacher_contact=models.CharField(max_length=20)
    teacher_course=models.ForeignKey(tbl_course,on_delete=models.CASCADE)
    teacher_photo=models.FileField(upload_to='TeacherPhoto/')
    teacher_college=models.ForeignKey(tbl_newcollege,on_delete=models.CASCADE)
    teacher_password=models.CharField(max_length=10,unique=True)
    election=models.ForeignKey(tbl_election,on_delete=models.CASCADE,null=True)
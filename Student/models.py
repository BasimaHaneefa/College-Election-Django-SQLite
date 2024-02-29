from django.db import models
from Guest.models import tbl_newstudent
from Admin.models import *


# Create your models here.
class tbl_complaint(models.Model):
    complaint_title=models.CharField(max_length=100)
    complaint_content=models.TextField()
    complaint_reply=models.TextField(default="Not Yet Viewed")
    complaint_date=models.DateField(auto_now_add=True)
    complaint_status=models.IntegerField(default=0)
    student=models.ForeignKey(tbl_newstudent,on_delete=models.CASCADE)

class tbl_feedback(models.Model):
    feedback_content=models.CharField(max_length=100)
    feedback_date=models.DateField(auto_now_add=True)    
    student=models.ForeignKey(tbl_newstudent,on_delete=models.CASCADE)

class tbl_classcandidate(models.Model):
    candidate_gender=models.CharField(max_length=1)
    candidate_status=models.IntegerField(default=0)
    candidate_election=models.ForeignKey(tbl_election,on_delete=models.CASCADE)
    candidate_student=models.ForeignKey(tbl_newstudent,on_delete=models.CASCADE)    

class tbl_classpolling(models.Model):
    polling_datetime=models.DateField(auto_now_add=True)
    polling_classcandidate=models.ForeignKey(tbl_classcandidate,on_delete=models.CASCADE)
    polling_student=models.ForeignKey(tbl_newstudent,on_delete=models.CASCADE)
    polling_status=models.IntegerField(default=0)    

class tbl_collegecandidate(models.Model):
    student=models.ForeignKey(tbl_newstudent,on_delete=models.CASCADE)    
    election=models.ForeignKey(tbl_election,on_delete=models.CASCADE)
    position=models.ForeignKey(tbl_position,on_delete=models.CASCADE)
    candidate_status=models.IntegerField(default=0)

class tbl_semmark(models.Model):
    sem1=models.CharField(max_length=20,default=0)
    sem2=models.CharField(max_length=20,default=0)
    sem3=models.CharField(max_length=20,default=0)
    candidate=models.ForeignKey(tbl_collegecandidate,on_delete=models.CASCADE)

class tbl_collegepolling(models.Model):
    polling_datetime=models.DateField(auto_now_add=True)
    chairperson_candidate=models.ForeignKey(tbl_collegecandidate,on_delete=models.CASCADE,null=True,related_name='chairperson')
    vchairperson_candidate=models.ForeignKey(tbl_collegecandidate,on_delete=models.CASCADE,null=True,related_name='vchairperson')
    general_candidate=models.ForeignKey(tbl_collegecandidate,on_delete=models.CASCADE,null=True,related_name='general')
    arts_candidate=models.ForeignKey(tbl_collegecandidate,on_delete=models.CASCADE,null=True,related_name='arts')
    first_candidate=models.ForeignKey(tbl_collegecandidate,on_delete=models.CASCADE,null=True,related_name='first')
    sec_candidate=models.ForeignKey(tbl_collegecandidate,on_delete=models.CASCADE,null=True,related_name='sec')
    third_candidate=models.ForeignKey(tbl_collegecandidate,on_delete=models.CASCADE,null=True,related_name='third')
    lady_candidate=models.ForeignKey(tbl_collegecandidate,on_delete=models.CASCADE,null=True,related_name='lady')
    editor_candidate=models.ForeignKey(tbl_collegecandidate,on_delete=models.CASCADE,null=True,related_name='editor')
    union_candidate=models.ForeignKey(tbl_collegecandidate,on_delete=models.CASCADE,null=True,related_name='union')
    polling_student=models.ForeignKey(tbl_newstudent,on_delete=models.CASCADE,null=True,related_name='students')
    polling_status=models.IntegerField(default=0)    

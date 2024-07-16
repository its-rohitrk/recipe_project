from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.conf import settings


from django.contrib.auth.models import User

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth import get_user_model
from  .manager import *
# User = get_user_model()


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15,unique=True)
    email = models.EmailField(unique=True)
    age = models.IntegerField(blank=True, null=True)

    objects = UserManager()


class Receipe (models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    receipe_name = models.CharField(max_length=100)
    receipe_description = models.TextField()
    receipe_img =  models.ImageField(upload_to="receipeimg")

class Department(models.Model):
    department = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.department
    class Meta:
        ordering = ['department']



class StudentId (models.Model):
    student_id = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.student_id



class Student(models.Model):
    department = models.ForeignKey(Department,related_name="depart" ,on_delete=models.CASCADE)
    student_id = models.OneToOneField(StudentId,related_name="studentid",on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField(unique=True)
    student_age = models.IntegerField(default=18)
    student_address  = models.TextField()
    def __str__(self) -> str:
        return self.student_name
    class Meta:
        ordering = ["student_name"]
        verbose_name = "student"



class Subject(models.Model):
    subject_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.subject_name

class SubjectMarks(models.Model):
    student = models.ForeignKey(Student,related_name="studentmarks",on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    marks = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.student.student_name} {self.subject.subject_name}'

    class Meta:
        unique_together = ("student","subject",)




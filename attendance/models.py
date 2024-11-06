from django.db import models

# Create your models here.

class Attendance(models.Model):
    fullname = models.CharField(max_length=100)

    phone    = models.CharField(max_length=100)

    email    = models.CharField(max_length=100)

    username = models.CharField(max_length=100)

    password = models.CharField(max_length=100)

    attendances=models.CharField(max_length=100)

    regnum=models.CharField(max_length=100)

    classesheld=models.CharField(max_length=100)

    courseandyear=models.CharField(max_length=100)

    date=models.CharField(max_length=100)

    status=models.CharField(max_length=100)

    sem1sub1=models.CharField(max_length=100)
   
    sem1sub2=models.CharField(max_length=100)
    
    sem1sub3=models.CharField(max_length=100)
    
    sem1sub4=models.CharField(max_length=100)
    
    sem2sub1=models.CharField(max_length=100)
    
    sem2sub2=models.CharField(max_length=100)
   
    sem2sub3=models.CharField(max_length=100)
    
    sem2sub4=models.CharField(max_length=100)

    sem1sub1att=models.IntegerField(default=0)
    sem1sub1held=models.IntegerField(default=0)

    sem1sub2att=models.IntegerField(default=0)
    sem1sub2held=models.IntegerField(default=0)

    sem1sub3att=models.IntegerField(default=0)
    sem1sub3held=models.IntegerField(default=0)

    sem1sub4att=models.IntegerField(default=0)
    sem1sub4held=models.IntegerField(default=0)

    sem2sub1att=models.IntegerField(default=0)
    sem2sub1held=models.IntegerField(default=0)

    sem2sub2att=models.IntegerField(default=0)
    sem2sub2held=models.IntegerField(default=0)

    sem2sub3att=models.IntegerField(default=0)
    sem2sub3held=models.IntegerField(default=0)

    sem2sub4att=models.IntegerField(default=0)
    sem2sub4held=models.IntegerField(default=0)


class Records(models.Model):

    copydate = models.CharField(max_length=100)
    copyname=models.CharField(max_length=100)
    copystatus=models.CharField(max_length=100)
    copyregnum=models.CharField(max_length=100)
    copycourse=models.CharField(max_length=100)
    copysub=models.CharField(max_length=100)


class Facultydb(models.Model):
    name = models.CharField(max_length=100)
    phone    = models.CharField(max_length=100)
    email    = models.CharField(max_length=100)
    assignedsub1 = models.CharField(max_length=100)
    assignedsub2 = models.CharField(max_length=100)
    assignedsub3 = models.CharField(max_length=100)
    assignedsub4 = models.CharField(max_length=100)
    staffid = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

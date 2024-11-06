from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Attendance
from .models import Facultydb
from .models import Records
import csv
import datetime

def facultylogin(request):
      return render(request, "attendance/facultylogin.html")

def login(request):
    if request.method == "POST":
        staffid   = request.POST.get("staffid")
        password   = request.POST.get("password")

        user = Facultydb.objects.filter(staffid=staffid, password=password)

        if user: 
            return render(request, "attendance/facultysection.html", {"user": user})
        else:
            msg = "Invalid username or password"
            return render(request, "attendance/facultylogin.html", {"msg": msg})

def facultysection(request):
      return render(request, "attendance/facultysection.html")

def allattendance(request):
    std=Attendance.objects.all()
    return render(request, "attendance/allattendance.html",{"allstudents":std})

def updateattendance(request, id):
    s=Attendance.objects.get(pk=id)
    return render(request, "attendance/updateattendance.html",{"singlestudent":s})

def doupdateattendance(request, id):
    updatedfullname = request.POST.get("fullname")
    updatedphone    = request.POST.get("phone")
    updatedemail    = request.POST.get("email")
    updatedusername = request.POST.get("username")
    updatedpassword = request.POST.get("password")
    updatedregister = request.POST.get("regnum")
    updatedcourseandyear = request.POST.get("courseandyear")
    s=Attendance.objects.get(pk=id)

    substr = "@gmail.com"

    if  updatedcourseandyear == "Course+Year":
        msg = "Select Course"
        return render(request, "attendance/updateattendance.html", {"message": msg, "singlestudent":s})
    elif len(updatedphone) <= 9 or len(updatedphone) >= 11:
        msg = "Enter a valid phone number"
        return render(request, "attendance/updateattendance.html", {"message2": msg, "singlestudent":s})
    elif  updatedphone[0] != "9" and updatedphone[0] != "8" and updatedphone[0] != "7" and updatedphone[0] != "6":
        msg = "Enter a valid phone number"
        return render(request, "attendance/updateattendance.html", {"message2": msg, "singlestudent":s})
    elif  substr not in updatedemail:
        msg = "Invalid email address"
        return render(request, "attendance/updateattendance.html", {"message3": msg, "singlestudent":s})
    else:

     s = Attendance.objects.get(pk=id)
     s.fullname = updatedfullname
     s.phone = updatedphone
     s.email = updatedemail
     s.username = updatedusername
     s.password = updatedpassword
     s.regnum = updatedregister
     s.courseandyear = updatedcourseandyear
     s.save()
     return redirect("/home")


def dashboard(request):
    return render(request, "attendance/dashboard.html")

def deletestudent(request, id):
    s= Attendance.objects.get(pk=id)
    s.delete()
    return redirect('showallattendancedetails')

def datewiseexcel(request):
    response = HttpResponse(content_type="text/csc")
    response['Content-Disposition'] = 'attachment;filename=DATEREC.csv'
    writer = csv.writer(response)
    tt =  Records.objects.all()
    writer.writerow([' ',' ','DATE RECORD','',' '])

    writer.writerow(['DATE','SUBJECT','NAME','STATUS'])
    for table in tt:
        writer.writerow([table.copydate,table.copysub,table.copyname,table.copystatus])
        return response
    
def studentdbexcel(request):
    response = HttpResponse(content_type="text/csc")
    response['Content-Disposition'] = 'attachment;filename=StudentDB.csv'
    writer = csv.writer(response)
    tt =  Attendance.objects.all()
    writer.writerow([' ',' ','STUDENT DATABASE',' ',' '])

    writer.writerow(['NAME','REG NO','COURSE&YEAR','PHONE','EMAIL'])
    for table in tt:
        writer.writerow([table.fullname,table.regnum,table.courseandyear,table.phone,table.email])
        return response
    
def facultydbexcel(request):
    response = HttpResponse(content_type="text/csc")
    response['Content-Disposition'] = 'attachment;filename=StaffDB.csv'
    writer = csv.writer(response)
    tt =  Facultydb.objects.all()
    writer.writerow([' ',' ','STAFF DATABASE',' ',' '])

    writer.writerow(['STAFF NAME','STAFF ID','PHONE NUMBER','EMAIL ADDRESS','ASSIGNED SUBJECT','ASSIGNED SUBJECT','ASSIGNED SUBJECT','ASSIGNED SUBJECT'])
    for table in tt:
        writer.writerow([table.name,table.staffid,table.phone,table.email,table.assignedsub1,table.assignedsub2,table.assignedsub3,table.assignedsub4])
        return response
    

def register(request):
    if request.method == "POST":
        # get all the values from the form . and store them 
        fullname = request.POST.get("fullname")
        regnum = request.POST.get("regnum")
        courseandyear = request.POST.get("courseandyear")
        phone    = request.POST.get("phone")
        email    = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        substr = "@gmail.com"

        match = Attendance.objects.filter(regnum=regnum)
        if match:
              msg = "Register number already exists"
              return render(request, "attendance/register.html", {"message": msg})
        elif len(phone) <= 9 or len(phone) >= 11:
              msg = "Enter a valid phone number"
              return render(request, "attendance/register.html", {"message2": msg})
        elif  phone[0] != "9" and phone[0] != "8" and phone[0] != "7" and phone[0] != "6":
              msg = "Enter a valid phone number"
              return render(request, "attendance/register.html", {"message2": msg})
        elif  substr not in email:
              msg = "Invalid email address"
              return render(request, "attendance/register.html", {"message3": msg})
        elif  courseandyear == "Course+Year":
              msg = "Select Course"
              return render(request, "attendance/register.html", {"message4": msg})
        else:
        # make an object of your Model class, Student 
         s = Attendance()
         s.fullname = fullname
         s.regnum = regnum
         s.courseandyear = courseandyear
         s.phone    = phone
         s.email    = email
         s.username = username
         s.password = password
         s.save()
         return redirect("/home")
    return render(request,"attendance/register.html")


def facultyregister(request):
    
    if request.method == "POST":
        # get all the values from the form . and store them 
        fullname = request.POST.get("fullname")
        phone    = request.POST.get("phone")
        email    = request.POST.get("email")
        assignedsub1 = request.POST.get("assignedsub1")
        assignedsub2 = request.POST.get("assignedsub2")
        assignedsub3 = request.POST.get("assignedsub3")
        assignedsub4 = request.POST.get("assignedsub4")
        staffid = request.POST.get("staffid")
        password = request.POST.get("password")

        substr = "@gmail.com"

        match = Facultydb.objects.filter(staffid=staffid)
        if match:
              msg = "Staff ID already exists"
              return render(request, "attendance/facultyregister.html", {"message": msg})
        elif len(staffid) > 5 or len(staffid) < 5:
              msg = "Enter a 5 digit staff ID"
              return render(request, "attendance/facultyregister.html", {"message": msg})
        elif len(phone) <= 9 or len(phone) >= 11:
              msg = "Enter a valid phone number"
              return render(request, "attendance/facultyregister.html", {"message2": msg})
        elif  phone[0] != "9" and phone[0] != "8" and phone[0] != "7" and phone[0] != "6":
              msg = "Enter a valid phone number"
              return render(request, "attendance/facultyregister.html", {"message2": msg})
        elif  substr not in email:
              msg = "Invalid email address"
              return render(request, "attendance/facultyregister.html", {"message3": msg})
        else:
        # make an object of your Model class, Student 
         s = Facultydb()
         s.name = fullname
         s.phone    = phone
         s.email    = email
         s.assignedsub1 = assignedsub1
         s.assignedsub2 = assignedsub2
         s.assignedsub3 = assignedsub3
         s.assignedsub4 = assignedsub4
         s.staffid = staffid
         s.password = password
         s.save()
         return redirect("/home")
    return render(request,"attendance/facultyregister.html")

def facultydb(request):
    std=Facultydb.objects.all()
    return render(request, "attendance/facultydb.html",{"allstaff":std})

def facultymanage(request):
    s=Facultydb.objects.all()
    if request.method == "POST":
    
     rno = request.POST.get("box")
     match = Facultydb.objects.filter(staffid=rno)
    
     return render(request, "attendance/facultymanage.html", {"match1":match, "alldata":s})
    else:
       nomatch=Facultydb.objects.all()
    return render(request, "attendance/facultymanage.html", {"nomatch1":nomatch, "alldata":s})


def facultyupdate(request, id):
    s=Facultydb.objects.get(pk=id)
    return render(request, "attendance/facultyupdate.html",{"singlestaff":s})

def doupdatefaculty(request, id):
        fullname = request.POST.get("fullname")
        phone    = request.POST.get("phone")
        email    = request.POST.get("email")
        assignedsub1 = request.POST.get("assignedsub1")
        assignedsub2 = request.POST.get("assignedsub2")
        assignedsub3 = request.POST.get("assignedsub3")
        assignedsub4 = request.POST.get("assignedsub4")
        staffid = request.POST.get("staffid")
        password = request.POST.get("password")
        s=Facultydb.objects.get(pk=id)

        substr = "@gmail.com"

        if len(phone) <= 9 or len(phone) >= 11:
              msg = "Enter a valid phone number"
              return render(request, "attendance/facultyregister.html", {"message2": msg})
        elif  phone[0] != "9" and phone[0] != "8" and phone[0] != "7" and phone[0] != "6":
              msg = "Enter a valid phone number"
              return render(request, "attendance/facultyregister.html", {"message2": msg})
        elif  substr not in email:
              msg = "Invalid email address"
              return render(request, "attendance/facultyregister.html", {"message3": msg})
        else:
         
         s = Facultydb.objects.get(pk=id)
         s.name = fullname
         s.phone    = phone
         s.email    = email
         s.assignedsub1 = assignedsub1
         s.assignedsub2 = assignedsub2
         s.assignedsub3 = assignedsub3
         s.assignedsub4 = assignedsub4
         s.staffid = staffid
         s.password = password
         s.save()
         return redirect("/facultymanage")

def deletefaculty(request, id):
    s= Facultydb.objects.get(pk=id)
    s.delete()
    return redirect('facultydb')

def facultylogin(request):
      return render(request, "attendance/facultylogin.html",)

def selectclass(request, id):
    
    s= Facultydb.objects.get(pk=id)
    sub1= s.assignedsub1
    sub2= s.assignedsub2
    sub3= s.assignedsub3
    sub4= s.assignedsub4
    return render(request, "attendance/selectclass.html", {'s': s, 'sub': sub1, 'sub4': sub4, 'sub3': sub3, 'sub2': sub2})


def viewrecords(request):
    
    return render(request, "attendance/viewrecords.html")

def viewbca1sub(request):
    BCA1=Attendance.objects.filter(courseandyear='BCA1')
    return render(request, "attendance/managesubjects.html",{"bca1":BCA1})

def viewbca2sub(request):
    BCA2=Attendance.objects.filter(courseandyear='BCA2')
    return render(request, "attendance/managesubjects.html",{"bca2":BCA2})

def viewbca3sub(request):
    BCA3=Attendance.objects.filter(courseandyear='BCA3')
    return render(request, "attendance/managesubjects.html",{"bca3":BCA3})

def viewbcom1sub(request):
    BCOM1=Attendance.objects.filter(courseandyear='BCOM1')
    return render(request, "attendance/managesubjects.html",{"bcom1":BCOM1})

def viewbcom2sub(request):
    BCOM2=Attendance.objects.filter(courseandyear='BCOM2')
    return render(request, "attendance/managesubjects.html",{"bcom2":BCOM2})

def viewbcom3sub(request):
    BCOM3=Attendance.objects.filter(courseandyear='BCOM3')
    return render(request, "attendance/managesubjects.html",{"bcom3":BCOM3})

def viewbba1sub(request):
    BBA1=Attendance.objects.filter(courseandyear='BBA1')
    return render(request, "attendance/managesubjects.html",{"bba1":BBA1})

def viewbba2sub(request):
    BBA2=Attendance.objects.filter(courseandyear='BBA2')
    return render(request, "attendance/managesubjects.html",{"bba2":BBA2})

def viewbba3sub(request):
    BBA3=Attendance.objects.filter(courseandyear='BBA3')
    return render(request, "attendance/managesubjects.html",{"bba3":BBA3})

def managesubjects(request):

    return render(request, "attendance/managesubjects.html")

def updatesubjects(request, id):
    sub=Attendance.objects.get(pk=id)

    return render(request, "attendance/updatesubjects.html", {"singleidsubs":sub})

def doupdatesubjects(request):

    if request.method == "POST":
     fetch = request.POST.get("courseandyear")
 
     updatedsem1sub1 = request.POST.get("sem1sub1")
     updatedsem1sub2 = request.POST.get("sem1sub2")
     updatedsem1sub3 = request.POST.get("sem1sub3")
     updatedsem1sub4 = request.POST.get("sem1sub4")
     updatedsem2sub1 = request.POST.get("sem2sub1")
     updatedsem2sub2 = request.POST.get("sem2sub2")
     updatedsem2sub3 = request.POST.get("sem2sub3")
     updatedsem2sub4 = request.POST.get("sem2sub4")

    S=Attendance.objects.filter(courseandyear=fetch)
    for eachS in S:

        eachS.sem1sub1 = updatedsem1sub1
        eachS.sem1sub2 = updatedsem1sub2
        eachS.sem1sub3 = updatedsem1sub3
        eachS.sem1sub4 = updatedsem1sub4
        eachS.sem2sub1 = updatedsem2sub1
        eachS.sem2sub2 = updatedsem2sub2
        eachS.sem2sub3 = updatedsem2sub3
        eachS.sem2sub4 = updatedsem2sub4
        eachS.save()
        

    return redirect("/managesubjects")



def viewbca1subs(request):
    BCA1=Attendance.objects.filter(courseandyear='BCA1')
    return render(request, "attendance/selectclass.html",{"bca1":BCA1})

def viewbca2subs(request):
    BCA2=Attendance.objects.filter(courseandyear='BCA2')
    return render(request, "attendance/selectclass.html",{"bca2":BCA2})

def viewbca3subs(request):
    BCA3=Attendance.objects.filter(courseandyear='BCA3')
    return render(request, "attendance/selectclass.html",{"bca3":BCA3})

def viewbcom1subs(request):
    BCOM1=Attendance.objects.filter(courseandyear='BCOM1')
    return render(request, "attendance/selectclass.html",{"bcom1":BCOM1})

def viewbcom2subs(request):
    BCOM2=Attendance.objects.filter(courseandyear='BCOM2')
    return render(request, "attendance/selectclass.html",{"bcom2":BCOM2})

def viewbcom3subs(request):
    BCOM3=Attendance.objects.filter(courseandyear='BCOM3')
    return render(request, "attendance/selectclass.html",{"bcom3":BCOM3})

def viewbba1subs(request):
    BBA1=Attendance.objects.filter(courseandyear='BBA1')
    return render(request, "attendance/selectclass.html",{"bba1":BBA1})

def viewbba2subs(request):
    BBA2=Attendance.objects.filter(courseandyear='BBA2')
    return render(request, "attendance/selectclass.html",{"bba2":BBA2})

def viewbba3subs(request):
    BBA3=Attendance.objects.filter(courseandyear='BBA3')
    return render(request, "attendance/selectclass.html",{"bba3":BBA3})



def s1s1present(request, id):
    s1= Attendance.objects.get(pk=id)
    val = int(s1.sem1sub1att) + 1
    val1 = int(s1.sem1sub1held) + 1
    s1.sem1sub1att=val
    s1.sem1sub1held=val1
    s1.status = "Present"
    s1.save()

    x=datetime.date.today()
    y = x.strftime("%d-%m-%Y")

    r = Records()
    r.copystatus = "Present"
    r.copyregnum = s1.regnum
    r.copyname = s1.fullname
    r.copycourse = s1.courseandyear
    r.copydate = y
    r.copysub = s1.sem1sub1
    r.save()

    course=s1.courseandyear
    if course == "BCA1":
            return redirect('/markclassattendancesub1bca1', {"s1":s1})

    elif course == "BCA2":
            return redirect('/markclassattendancesub1bca2', {"s1":s1})

    elif course == "BCA3":
            return redirect('/markclassattendancesub1bca3', {"s1":s1})

    elif course == "BCOM1":
            return redirect('/markclassattendancesub1bcom1', {"s1":s1})

    elif course == "BCOM2":
            return redirect('/markclassattendancesub1bcom2', {"s1":s1})

    elif course == "BCOM3":
            return redirect('/markclassattendancesub1bcom3', {"s1":s1})

    elif course == "BBA1":
            return redirect('/markclassattendancesub1bba1', {"s1":s1})

    elif course == "BBA2":
            return redirect('/markclassattendancesub1bba2', {"s1":s1})

    elif course == "BBA3":
    
         return redirect('/markclassattendancesub1bba3', {"s1":s1})

def s1s1absent(request, id):
    s1= Attendance.objects.get(pk=id)
    s1.sem1sub1held=int(s1.sem1sub1held)+1
    s1.status="Absent"
    s1.save()

    x=datetime.date.today()
    y = x.strftime("%d-%m-%Y")

    r = Records()
    r.copystatus = "Absent"
    r.copyregnum = s1.regnum
    r.copyname = s1.fullname
    r.copycourse = s1.courseandyear
    r.copydate = y
    r.copysub = s1.sem1sub1

    r.save()
    
    course=s1.courseandyear
    if course == "BCA1":
            return redirect('/markclassattendancesub1bca1', {"s1":s1})

    elif course == "BCA2":
            return redirect('/markclassattendancesub1bca2', {"s1":s1})

    elif course == "BCA3":
            return redirect('/markclassattendancesub1bca3', {"s1":s1})

    elif course == "BCOM1":
            return redirect('/markclassattendancesub1bcom1', {"s1":s1})

    elif course == "BCOM2":
            return redirect('/markclassattendancesub1bcom2', {"s1":s1})

    elif course == "BCOM3":
            return redirect('/markclassattendancesub1bcom3', {"s1":s1})

    elif course == "BBA1":
            return redirect('/markclassattendancesub1bba1', {"s1":s1})

    elif course == "BBA2":
            return redirect('/markclassattendancesub1bba2', {"s1":s1})

    elif course == "BBA3":
    
         return redirect('/markclassattendancesub1bba3', {"s1":s1})

def s1s2present(request, id):
    s1= Attendance.objects.get(pk=id)
    val = int(s1.sem1sub2att) + 1
    val1 = int(s1.sem1sub2held) + 1
    s1.sem1sub2att=val
    s1.sem1sub2held=val1
    s1.status = "Present"
    s1.save()

    x=datetime.date.today()
    y = x.strftime("%d-%m-%Y")

    r = Records()
    r.copystatus = "Present"
    r.copyregnum = s1.regnum
    r.copyname = s1.fullname
    r.copycourse = s1.courseandyear
    r.copydate = y
    r.copysub = s1.sem1sub2
    r.save()

    course=s1.courseandyear
    if course == "BCA1":
            return redirect('/markclassattendancesub2bca1', {"s1":s1})

    elif course == "BCA2":
            return redirect('/markclassattendancesub2bca2', {"s1":s1})

    elif course == "BCA3":
            return redirect('/markclassattendancesub2bca3', {"s1":s1})

    elif course == "BCOM1":
            return redirect('/markclassattendancesub2bcom1', {"s1":s1})

    elif course == "BCOM2":
            return redirect('/markclassattendancesub2bcom2', {"s1":s1})

    elif course == "BCOM3":
            return redirect('/markclassattendancesub2bcom3', {"s1":s1})

    elif course == "BBA1":
            return redirect('/markclassattendancesub2bba1', {"s1":s1})

    elif course == "BBA2":
            return redirect('/markclassattendancesub2bba2', {"s1":s1})

    elif course == "BBA3":
    
         return redirect('/markclassattendancesub2bba3', {"s1":s1})

def s1s2absent(request, id):
    s1= Attendance.objects.get(pk=id)
    s1.sem1sub2held=int(s1.sem1sub2held)+1
    s1.status="Absent"
    s1.save()

    x=datetime.date.today()
    y = x.strftime("%d-%m-%Y")

    r = Records()
    r.copystatus = "Absent"
    r.copyregnum = s1.regnum
    r.copyname = s1.fullname
    r.copycourse = s1.courseandyear
    r.copydate = y
    r.copysub = s1.sem1sub2
    r.save()
    
    course=s1.courseandyear
    if course == "BCA1":
            return redirect('/markclassattendancesub2bca1', {"s1":s1})

    elif course == "BCA2":
            return redirect('/markclassattendancesub2bca2', {"s1":s1})

    elif course == "BCA3":
            return redirect('/markclassattendancesub2bca3', {"s1":s1})

    elif course == "BCOM1":
            return redirect('/markclassattendancesub2bcom1', {"s1":s1})

    elif course == "BCOM2":
            return redirect('/markclassattendancesub2bcom2', {"s1":s1})

    elif course == "BCOM3":
            return redirect('/markclassattendancesub2bcom3', {"s1":s1})

    elif course == "BBA1":
            return redirect('/markclassattendancesub2bba1', {"s1":s1})

    elif course == "BBA2":
            return redirect('/markclassattendancesub2bba2', {"s1":s1})

    elif course == "BBA3":
    
         return redirect('/markclassattendancesub2bba3', {"s1":s1})
    return redirect('markclassattendancesub2')

def s1s3present(request, id):
    s1= Attendance.objects.get(pk=id)
    val = int(s1.sem1sub3att) + 1
    val1 = int(s1.sem1sub3held) + 1
    s1.sem1sub3att=val
    s1.sem1sub3held=val1
    s1.status = "Present"
    s1.save()

    x=datetime.date.today()
    y = x.strftime("%d-%m-%Y")

    r = Records()
    r.copystatus = "Present"
    r.copyregnum = s1.regnum
    r.copyname = s1.fullname
    r.copycourse = s1.courseandyear
    r.copydate = y
    r.copysub = s1.sem1sub3
    r.save()

    course=s1.courseandyear
    if course == "BCA1":
            return redirect('/markclassattendancesub3bca1', {"s1":s1})

    elif course == "BCA2":
            return redirect('/markclassattendancesub3bca2', {"s1":s1})

    elif course == "BCA3":
            return redirect('/markclassattendancesub3bca3', {"s1":s1})

    elif course == "BCOM1":
            return redirect('/markclassattendancesub3bcom1', {"s1":s1})

    elif course == "BCOM2":
            return redirect('/markclassattendancesub3bcom2', {"s1":s1})

    elif course == "BCOM3":
            return redirect('/markclassattendancesub3bcom3', {"s1":s1})

    elif course == "BBA1":
            return redirect('/markclassattendancesub3bba1', {"s1":s1})

    elif course == "BBA2":
            return redirect('/markclassattendancesub3bba2', {"s1":s1})

    elif course == "BBA3":
    
         return redirect('/markclassattendancesub3bba3', {"s1":s1})

def s1s3absent(request, id):
    s1= Attendance.objects.get(pk=id)
    s1.sem1sub3held=int(s1.sem1sub3held)+1
    s1.status="Absent"
    s1.save()

    x=datetime.date.today()
    y = x.strftime("%d-%m-%Y")

    r = Records()
    r.copystatus = "Absent"
    r.copyregnum = s1.regnum
    r.copyname = s1.fullname
    r.copycourse = s1.courseandyear
    r.copydate = y
    r.copysub = s1.sem1sub3
    r.save()
    
    course=s1.courseandyear
    if course == "BCA1":
            return redirect('/markclassattendancesub3bca1', {"s1":s1})

    elif course == "BCA2":
            return redirect('/markclassattendancesub3bca2', {"s1":s1})

    elif course == "BCA3":
            return redirect('/markclassattendancesub3bca3', {"s1":s1})

    elif course == "BCOM1":
            return redirect('/markclassattendancesub3bcom1', {"s1":s1})

    elif course == "BCOM2":
            return redirect('/markclassattendancesub3bcom2', {"s1":s1})

    elif course == "BCOM3":
            return redirect('/markclassattendancesub3bcom3', {"s1":s1})

    elif course == "BBA1":
            return redirect('/markclassattendancesub3bba1', {"s1":s1})

    elif course == "BBA2":
            return redirect('/markclassattendancesub3bba2', {"s1":s1})

    elif course == "BBA3":
    
         return redirect('/markclassattendancesub3bba3', {"s1":s1})
    
def s1s4present(request, id):
    s1= Attendance.objects.get(pk=id)
    val = int(s1.sem1sub4att) + 1
    val1 = int(s1.sem1sub4held) + 1
    s1.sem1sub4att=val
    s1.sem1sub4held=val1
    s1.status = "Present"
    s1.save()

    x=datetime.date.today()
    y = x.strftime("%d-%m-%Y")

    r = Records()
    r.copystatus = "Present"
    r.copyregnum = s1.regnum
    r.copyname = s1.fullname
    r.copycourse = s1.courseandyear
    r.copydate = y
    r.copysub = s1.sem1sub4
    r.save()

    course=s1.courseandyear
    if course == "BCA1":
            return redirect('/markclassattendancesub4bca1', {"s1":s1})

    elif course == "BCA2":
            return redirect('/markclassattendancesub4bca2', {"s1":s1})

    elif course == "BCA3":
            return redirect('/markclassattendancesub4bca3', {"s1":s1})

    elif course == "BCOM1":
            return redirect('/markclassattendancesub4bcom1', {"s1":s1})

    elif course == "BCOM2":
            return redirect('/markclassattendancesub4bcom2', {"s1":s1})

    elif course == "BCOM3":
            return redirect('/markclassattendancesub4bcom3', {"s1":s1})

    elif course == "BBA1":
            return redirect('/markclassattendancesub4bba1', {"s1":s1})

    elif course == "BBA2":
            return redirect('/markclassattendancesub4bba2', {"s1":s1})

    elif course == "BBA3":
    
         return redirect('/markclassattendancesub4bba3', {"s1":s1})

def s1s4absent(request, id):
    s1= Attendance.objects.get(pk=id)
    s1.sem1sub4held=int(s1.sem1sub4held)+1
    s1.status="Absent"
    s1.save()

    x=datetime.date.today()
    y = x.strftime("%d-%m-%Y")

    r = Records()
    r.copystatus = "Absent"
    r.copyregnum = s1.regnum
    r.copyname = s1.fullname
    r.copycourse = s1.courseandyear
    r.copydate = y
    r.copysub = s1.sem1sub4
    r.save()
    
    course=s1.courseandyear
    if course == "BCA1":
            return redirect('/markclassattendancesub4bca1', {"s1":s1})

    elif course == "BCA2":
            return redirect('/markclassattendancesub4bca2', {"s1":s1})

    elif course == "BCA3":
            return redirect('/markclassattendancesub4bca3', {"s1":s1})

    elif course == "BCOM1":
            return redirect('/markclassattendancesub4bcom1', {"s1":s1})

    elif course == "BCOM2":
            return redirect('/markclassattendancesub4bcom2', {"s1":s1})

    elif course == "BCOM3":
            return redirect('/markclassattendancesub4bcom3', {"s1":s1})

    elif course == "BBA1":
            return redirect('/markclassattendancesub4bba1', {"s1":s1})

    elif course == "BBA2":
            return redirect('/markclassattendancesub4bba2', {"s1":s1})

    elif course == "BBA3":
    
         return redirect('/markclassattendancesub4bba3', {"s1":s1})

def s2s1present(request, id):
    s1= Attendance.objects.get(pk=id)
    val = int(s1.sem2sub1att) + 1
    val1 = int(s1.sem2sub1held) + 1
    s1.sem2sub1att=val
    s1.sem2sub1held=val1
    s1.status = "Present"
    s1.save()

    x=datetime.date.today()
    y = x.strftime("%d-%m-%Y")

    r = Records()
    r.copystatus = "Present"
    r.copyregnum = s1.regnum
    r.copyname = s1.fullname
    r.copycourse = s1.courseandyear
    r.copydate = y
    r.copysub = s1.sem2sub1
    r.save()

    course=s1.courseandyear
    if course == "BCA1":
            return redirect('/markclassattendancesub5bca1', {"s1":s1})

    elif course == "BCA2":
            return redirect('/markclassattendancesub5bca2', {"s1":s1})

    elif course == "BCA3":
            return redirect('/markclassattendancesub5bca3', {"s1":s1})

    elif course == "BCOM1":
            return redirect('/markclassattendancesub5bcom1', {"s1":s1})

    elif course == "BCOM2":
            return redirect('/markclassattendancesub5bcom2', {"s1":s1})

    elif course == "BCOM3":
            return redirect('/markclassattendancesub5bcom3', {"s1":s1})

    elif course == "BBA1":
            return redirect('/markclassattendancesub5bba1', {"s1":s1})

    elif course == "BBA2":
            return redirect('/markclassattendancesub5bba2', {"s1":s1})

    elif course == "BBA3":
    
         return redirect('/markclassattendancesub5bba3', {"s1":s1})

def s2s1absent(request, id):
    s1= Attendance.objects.get(pk=id)
    s1.sem2sub1held=int(s1.sem2sub1held)+1
    s1.status="Absent"
    s1.save()

    x=datetime.date.today()
    y = x.strftime("%d-%m-%Y")

    r = Records()
    r.copystatus = "Absent"
    r.copyregnum = s1.regnum
    r.copyname = s1.fullname
    r.copycourse = s1.courseandyear
    r.copydate = y
    r.copysub = s1.sem2sub1
    r.save()
    
    course=s1.courseandyear
    if course == "BCA1":
            return redirect('/markclassattendancesub5bca1', {"s1":s1})

    elif course == "BCA2":
            return redirect('/markclassattendancesub5bca2', {"s1":s1})

    elif course == "BCA3":
            return redirect('/markclassattendancesub5bca3', {"s1":s1})

    elif course == "BCOM1":
            return redirect('/markclassattendancesub5bcom1', {"s1":s1})

    elif course == "BCOM2":
            return redirect('/markclassattendancesub5bcom2', {"s1":s1})

    elif course == "BCOM3":
            return redirect('/markclassattendancesub5bcom3', {"s1":s1})

    elif course == "BBA1":
            return redirect('/markclassattendancesub5bba1', {"s1":s1})

    elif course == "BBA2":
            return redirect('/markclassattendancesub5bba2', {"s1":s1})

    elif course == "BBA3":
    
         return redirect('/markclassattendancesub5bba3', {"s1":s1})

def s2s2present(request, id):
    s1= Attendance.objects.get(pk=id)
    val = int(s1.sem2sub2att) + 1
    val1 = int(s1.sem2sub2held) + 1
    s1.sem2sub2att=val
    s1.sem2sub2held=val1
    s1.status = "Present"
    s1.save()


    x=datetime.date.today()
    y = x.strftime("%d-%m-%Y")

    r = Records()
    r.copystatus = "Present"
    r.copyregnum = s1.regnum
    r.copyname = s1.fullname
    r.copycourse = s1.courseandyear
    r.copydate = y
    r.copysub = s1.sem2sub2
    r.save()

    course=s1.courseandyear
    if course == "BCA1":
            return redirect('/markclassattendancesub6bca1', {"s1":s1})

    elif course == "BCA2":
            return redirect('/markclassattendancesub6bca2', {"s1":s1})

    elif course == "BCA3":
            return redirect('/markclassattendancesub6bca3', {"s1":s1})

    elif course == "BCOM1":
            return redirect('/markclassattendancesub6bcom1', {"s1":s1})

    elif course == "BCOM2":
            return redirect('/markclassattendancesub6bcom2', {"s1":s1})

    elif course == "BCOM3":
            return redirect('/markclassattendancesub6bcom3', {"s1":s1})

    elif course == "BBA1":
            return redirect('/markclassattendancesub6bba1', {"s1":s1})

    elif course == "BBA2":
            return redirect('/markclassattendancesub6bba2', {"s1":s1})

    elif course == "BBA3":
    
         return redirect('/markclassattendancesub6bba3', {"s1":s1})

def s2s2absent(request, id):
    s1= Attendance.objects.get(pk=id)
    s1.sem2sub2held=int(s1.sem2sub2held)+1
    s1.status="Absent"
    s1.save()

    x=datetime.date.today()
    y = x.strftime("%d-%m-%Y")

    r = Records()
    r.copystatus = "Absent"
    r.copyregnum = s1.regnum
    r.copyname = s1.fullname
    r.copycourse = s1.courseandyear
    r.copydate = y
    r.copysub = s1.sem2sub2
    r.save()
    
    course=s1.courseandyear
    if course == "BCA1":
            return redirect('/markclassattendancesub6bca1', {"s1":s1})

    elif course == "BCA2":
            return redirect('/markclassattendancesub6bca2', {"s1":s1})

    elif course == "BCA3":
            return redirect('/markclassattendancesub6bca3', {"s1":s1})

    elif course == "BCOM1":
            return redirect('/markclassattendancesub6bcom1', {"s1":s1})

    elif course == "BCOM2":
            return redirect('/markclassattendancesub6bcom2', {"s1":s1})

    elif course == "BCOM3":
            return redirect('/markclassattendancesub6bcom3', {"s1":s1})

    elif course == "BBA1":
            return redirect('/markclassattendancesub6bba1', {"s1":s1})

    elif course == "BBA2":
            return redirect('/markclassattendancesub6bba2', {"s1":s1})

    elif course == "BBA3":
    
         return redirect('/markclassattendancesub6bba3', {"s1":s1})

def s2s3present(request, id):
    s1= Attendance.objects.get(pk=id)
    val = int(s1.sem2sub3att) + 1
    val1 = int(s1.sem2sub3held) + 1
    s1.sem2sub3att=val
    s1.sem2sub3held=val1
    s1.status = "Present"
    s1.save()

    x=datetime.date.today()
    y = x.strftime("%d-%m-%Y")

    r = Records()
    r.copystatus = "Present"
    r.copyregnum = s1.regnum
    r.copyname = s1.fullname
    r.copycourse = s1.courseandyear
    r.copydate = y
    r.copysub = s1.sem2sub3
    r.save()

    course=s1.courseandyear
    if course == "BCA1":
            return redirect('/markclassattendancesub7bca1', {"s1":s1})

    elif course == "BCA2":
            return redirect('/markclassattendancesub7bca2', {"s1":s1})

    elif course == "BCA3":
            return redirect('/markclassattendancesub7bca3', {"s1":s1})

    elif course == "BCOM1":
            return redirect('/markclassattendancesub7bcom1', {"s1":s1})

    elif course == "BCOM2":
            return redirect('/markclassattendancesub7bcom2', {"s1":s1})

    elif course == "BCOM3":
            return redirect('/markclassattendancesub7bcom3', {"s1":s1})

    elif course == "BBA1":
            return redirect('/markclassattendancesub7bba1', {"s1":s1})

    elif course == "BBA2":
            return redirect('/markclassattendancesub7bba2', {"s1":s1})

    elif course == "BBA3":
    
         return redirect('/markclassattendancesub7bba3', {"s1":s1})

def s2s3absent(request, id):
    s1= Attendance.objects.get(pk=id)
    s1.sem2sub3held=int(s1.sem2sub3held)+1
    s1.status="Absent"
    s1.save()

    x=datetime.date.today()
    y = x.strftime("%d-%m-%Y")

    r = Records()
    r.copystatus = "Absent"
    r.copyregnum = s1.regnum
    r.copyname = s1.fullname
    r.copycourse = s1.courseandyear
    r.copydate = y
    r.copysub = s1.sem2sub3
    r.save()

    course=s1.courseandyear
    if course == "BCA1":
            return redirect('/markclassattendancesub7bca1', {"s1":s1})

    elif course == "BCA2":
            return redirect('/markclassattendancesub7bca2', {"s1":s1})

    elif course == "BCA3":
            return redirect('/markclassattendancesub7bca3', {"s1":s1})

    elif course == "BCOM1":
            return redirect('/markclassattendancesub7bcom1', {"s1":s1})

    elif course == "BCOM2":
            return redirect('/markclassattendancesub7bcom2', {"s1":s1})

    elif course == "BCOM3":
            return redirect('/markclassattendancesub7bcom3', {"s1":s1})

    elif course == "BBA1":
            return redirect('/markclassattendancesub7bba1', {"s1":s1})

    elif course == "BBA2":
            return redirect('/markclassattendancesub7bba2', {"s1":s1})

    elif course == "BBA3":
    
         return redirect('/markclassattendancesub7bba3', {"s1":s1})

def s2s4present(request, id):
    s1= Attendance.objects.get(pk=id)
    val = int(s1.sem2sub4att) + 1
    val1 = int(s1.sem2sub4held) + 1
    s1.sem2sub4att=val
    s1.sem2sub4held=val1
    s1.status = "Present"
    s1.save()

    x=datetime.date.today()
    y = x.strftime("%d-%m-%Y")

    r = Records()
    r.copystatus = "Present"
    r.copyregnum = s1.regnum
    r.copyname = s1.fullname
    r.copycourse = s1.courseandyear
    r.copydate = y
    r.copysub = s1.sem2sub4
    r.save()

    course=s1.courseandyear
    if course == "BCA1":
            return redirect('/markclassattendancesub8bca1', {"s1":s1})

    elif course == "BCA2":
            return redirect('/markclassattendancesub8bca2', {"s1":s1})

    elif course == "BCA3":
            return redirect('/markclassattendancesub8bca3', {"s1":s1})

    elif course == "BCOM1":
            return redirect('/markclassattendancesub8bcom1', {"s1":s1})

    elif course == "BCOM2":
            return redirect('/markclassattendancesub8bcom2', {"s1":s1})

    elif course == "BCOM3":
            return redirect('/markclassattendancesub8bcom3', {"s1":s1})

    elif course == "BBA1":
            return redirect('/markclassattendancesub8bba1', {"s1":s1})

    elif course == "BBA2":
            return redirect('/markclassattendancesub8bba2', {"s1":s1})

    elif course == "BBA3":
    
         return redirect('/markclassattendancesub8bba3', {"s1":s1})

def s2s4absent(request, id):
    s1= Attendance.objects.get(pk=id)
    s1.sem2sub4held=int(s1.sem2sub4held)+1
    s1.status="Absent"
    s1.save()

    x=datetime.date.today()
    y = x.strftime("%d-%m-%Y")

    r = Records()
    r.copystatus = "Absent"
    r.copyregnum = s1.regnum
    r.copyname = s1.fullname
    r.copycourse = s1.courseandyear
    r.copydate = y
    r.copysub = s1.sem2sub4
    r.save()

    course=s1.courseandyear
    if course == "BCA1":
            return redirect('/markclassattendancesub8bca1', {"s1":s1})

    elif course == "BCA2":
            return redirect('/markclassattendancesub8bca2', {"s1":s1})

    elif course == "BCA3":
            return redirect('/markclassattendancesub8bca3', {"s1":s1})

    elif course == "BCOM1":
            return redirect('/markclassattendancesub8bcom1', {"s1":s1})

    elif course == "BCOM2":
            return redirect('/markclassattendancesub8bcom2', {"s1":s1})

    elif course == "BCOM3":
            return redirect('/markclassattendancesub8bcom3', {"s1":s1})

    elif course == "BBA1":
            return redirect('/markclassattendancesub8bba1', {"s1":s1})

    elif course == "BBA2":
            return redirect('/markclassattendancesub8bba2', {"s1":s1})

    elif course == "BBA3":
    
         return redirect('/markclassattendancesub8bba3', {"s1":s1})





def markclassattendancesub1bca1(request):
    BCA1=Attendance.objects.filter(courseandyear='BCA1')
    return render(request, "attendance/markclassattendancesub1.html",{"bca1":BCA1}) 

def markclassattendancesub1bca2(request):

    BCA2=Attendance.objects.filter(courseandyear='BCA2')

    return render(request, "attendance/markclassattendancesub1.html",{"bca2":BCA2})

def markclassattendancesub1bca3(request):

    BCA3=Attendance.objects.filter(courseandyear='BCA3')

    return render(request, "attendance/markclassattendancesub1.html",{"bca3":BCA3})

def markclassattendancesub1bcom1(request):

    BCOM1=Attendance.objects.filter(courseandyear='BCOM1')

    return render(request, "attendance/markclassattendancesub1.html",{"bcom1":BCOM1})

def markclassattendancesub1bcom2(request):

    BCOM2=Attendance.objects.filter(courseandyear='BCOM2')

    return render(request, "attendance/markclassattendancesub1.html",{"bcom2":BCOM2})

def markclassattendancesub1bcom3(request):

    BCOM3=Attendance.objects.filter(courseandyear='BCOM3')

    return render(request, "attendance/markclassattendancesub1.html",{"bcom3":BCOM3})

def markclassattendancesub1bba1(request):

    BBA1=Attendance.objects.filter(courseandyear='BBA1')

    return render(request, "attendance/markclassattendancesub1.html",{"bba1":BBA1})

def markclassattendancesub1bba2(request):

    BBA2=Attendance.objects.filter(courseandyear='BBA2')

    return render(request, "attendance/markclassattendancesub1.html",{"bba2":BBA2})

def markclassattendancesub1bba3(request):

    BBA3=Attendance.objects.filter(courseandyear='BBA3')

    return render(request, "attendance/markclassattendancesub1.html",{"bba3":BBA3})



def markclassattendancesub2bca1(request):

    BCA1=Attendance.objects.filter(courseandyear='BCA1')

    return render(request, "attendance/markclassattendancesub2.html",{"bca1":BCA1})

def markclassattendancesub2bca2(request):

    BCA2=Attendance.objects.filter(courseandyear='BCA2')

    return render(request, "attendance/markclassattendancesub2.html",{"bca2":BCA2})

def markclassattendancesub2bca3(request):

    BCA3=Attendance.objects.filter(courseandyear='BCA3')

    return render(request, "attendance/markclassattendancesub2.html",{"bca3":BCA3})

def markclassattendancesub2bcom1(request):

    BCOM1=Attendance.objects.filter(courseandyear='BCOM1')

    return render(request, "attendance/markclassattendancesub2.html",{"bcom1":BCOM1})

def markclassattendancesub2bcom2(request):

    BCOM2=Attendance.objects.filter(courseandyear='BCOM2')

    return render(request, "attendance/markclassattendancesub2.html",{"bcom2":BCOM2})

def markclassattendancesub2bcom3(request):

    BCOM3=Attendance.objects.filter(courseandyear='BCOM3')

    return render(request, "attendance/markclassattendancesub2.html",{"bcom3":BCOM3})

def markclassattendancesub2bba1(request):

    BBA1=Attendance.objects.filter(courseandyear='BBA1')

    return render(request, "attendance/markclassattendancesub2.html",{"bba1":BBA1})

def markclassattendancesub2bba2(request):

    BBA2=Attendance.objects.filter(courseandyear='BBA2')

    return render(request, "attendance/markclassattendancesub2.html",{"bba2":BBA2})

def markclassattendancesub2bba3(request):

    BBA3=Attendance.objects.filter(courseandyear='BBA3')

    return render(request, "attendance/markclassattendancesub2.html",{"bba3":BBA3})



def markclassattendancesub3bca1(request):

    BCA1=Attendance.objects.filter(courseandyear='BCA1')

    return render(request, "attendance/markclassattendancesub3.html",{"bca1":BCA1})

def markclassattendancesub3bca2(request):

    BCA2=Attendance.objects.filter(courseandyear='BCA2')

    return render(request, "attendance/markclassattendancesub3.html",{"bca2":BCA2})

def markclassattendancesub3bca3(request):

    BCA3=Attendance.objects.filter(courseandyear='BCA3')

    return render(request, "attendance/markclassattendancesub3.html",{"bca3":BCA3})

def markclassattendancesub3bcom1(request):

    BCOM1=Attendance.objects.filter(courseandyear='BCOM1')

    return render(request, "attendance/markclassattendancesub3.html",{"bcom1":BCOM1})

def markclassattendancesub3bcom2(request):

    BCOM2=Attendance.objects.filter(courseandyear='BCOM2')

    return render(request, "attendance/markclassattendancesub3.html",{"bcom2":BCOM2})

def markclassattendancesub3bcom3(request):

    BCOM3=Attendance.objects.filter(courseandyear='BCOM3')

    return render(request, "attendance/markclassattendancesub3.html",{"bcom3":BCOM3})

def markclassattendancesub3bba1(request):

    BBA1=Attendance.objects.filter(courseandyear='BBA1')

    return render(request, "attendance/markclassattendancesub3.html",{"bba1":BBA1})

def markclassattendancesub3bba2(request):

    BBA2=Attendance.objects.filter(courseandyear='BBA2')

    return render(request, "attendance/markclassattendancesub3.html",{"bba2":BBA2})

def markclassattendancesub3bba3(request):

    BBA3=Attendance.objects.filter(courseandyear='BBA3')

    return render(request, "attendance/markclassattendancesub3.html",{"bba3":BBA3})



def markclassattendancesub4bca1(request):

    BCA1=Attendance.objects.filter(courseandyear='BCA1')

    return render(request, "attendance/markclassattendancesub4.html",{"bca1":BCA1})

def markclassattendancesub4bca2(request):

    BCA2=Attendance.objects.filter(courseandyear='BCA2')

    return render(request, "attendance/markclassattendancesub4.html",{"bca2":BCA2})

def markclassattendancesub4bca3(request):

    BCA3=Attendance.objects.filter(courseandyear='BCA3')

    return render(request, "attendance/markclassattendancesub4.html",{"bca3":BCA3})

def markclassattendancesub4bcom1(request):

    BCOM1=Attendance.objects.filter(courseandyear='BCOM1')

    return render(request, "attendance/markclassattendancesub4.html",{"bcom1":BCOM1})

def markclassattendancesub4bcom2(request):

    BCOM2=Attendance.objects.filter(courseandyear='BCOM2')

    return render(request, "attendance/markclassattendancesub4.html",{"bcom2":BCOM2})

def markclassattendancesub4bcom3(request):

    BCOM3=Attendance.objects.filter(courseandyear='BCOM3')

    return render(request, "attendance/markclassattendancesub4.html",{"bcom3":BCOM3})

def markclassattendancesub4bba1(request):

    BBA1=Attendance.objects.filter(courseandyear='BBA1')

    return render(request, "attendance/markclassattendancesub4.html",{"bba1":BBA1})

def markclassattendancesub4bba2(request):

    BBA2=Attendance.objects.filter(courseandyear='BBA2')

    return render(request, "attendance/markclassattendancesub4.html",{"bba2":BBA2})

def markclassattendancesub4bba3(request):

    BBA3=Attendance.objects.filter(courseandyear='BBA3')

    return render(request, "attendance/markclassattendancesub4.html",{"bba3":BBA3})



def markclassattendancesub5bca1(request):

    BCA1=Attendance.objects.filter(courseandyear='BCA1')

    return render(request, "attendance/markclassattendancesub5.html",{"bca1":BCA1})

def markclassattendancesub5bca2(request):

    BCA2=Attendance.objects.filter(courseandyear='BCA2')

    return render(request, "attendance/markclassattendancesub5.html",{"bca2":BCA2})

def markclassattendancesub5bca3(request):

    BCA3=Attendance.objects.filter(courseandyear='BCA3')

    return render(request, "attendance/markclassattendancesub5.html",{"bca3":BCA3})

def markclassattendancesub5bcom1(request):

    BCOM1=Attendance.objects.filter(courseandyear='BCOM1')

    return render(request, "attendance/markclassattendancesub5.html",{"bcom1":BCOM1})

def markclassattendancesub5bcom2(request):

    BCOM2=Attendance.objects.filter(courseandyear='BCOM2')

    return render(request, "attendance/markclassattendancesub5.html",{"bcom2":BCOM2})

def markclassattendancesub5bcom3(request):

    BCOM3=Attendance.objects.filter(courseandyear='BCOM3')

    return render(request, "attendance/markclassattendancesub5.html",{"bcom3":BCOM3})

def markclassattendancesub5bba1(request):

    BBA1=Attendance.objects.filter(courseandyear='BBA1')

    return render(request, "attendance/markclassattendancesub5.html",{"bba1":BBA1})

def markclassattendancesub5bba2(request):

    BBA2=Attendance.objects.filter(courseandyear='BBA2')

    return render(request, "attendance/markclassattendancesub5.html",{"bba2":BBA2})

def markclassattendancesub5bba3(request):

    BBA3=Attendance.objects.filter(courseandyear='BBA3')

    return render(request, "attendance/markclassattendancesub5.html",{"bba3":BBA3})



def markclassattendancesub6bca1(request):

    BCA1=Attendance.objects.filter(courseandyear='BCA1')

    return render(request, "attendance/markclassattendancesub6.html",{"bca1":BCA1})

def markclassattendancesub6bca2(request):

    BCA2=Attendance.objects.filter(courseandyear='BCA2')

    return render(request, "attendance/markclassattendancesub6.html",{"bca2":BCA2})

def markclassattendancesub6bca3(request):

    BCA3=Attendance.objects.filter(courseandyear='BCA3')

    return render(request, "attendance/markclassattendancesub6.html",{"bca3":BCA3})

def markclassattendancesub6bcom1(request):

    BCOM1=Attendance.objects.filter(courseandyear='BCOM1')

    return render(request, "attendance/markclassattendancesub6.html",{"bcom1":BCOM1})

def markclassattendancesub6bcom2(request):

    BCOM2=Attendance.objects.filter(courseandyear='BCOM2')

    return render(request, "attendance/markclassattendancesub6.html",{"bcom2":BCOM2})

def markclassattendancesub6bcom3(request):

    BCOM3=Attendance.objects.filter(courseandyear='BCOM3')

    return render(request, "attendance/markclassattendancesub6.html",{"bcom3":BCOM3})

def markclassattendancesub6bba1(request):

    BBA1=Attendance.objects.filter(courseandyear='BBA1')

    return render(request, "attendance/markclassattendancesub6.html",{"bba1":BBA1})

def markclassattendancesub6bba2(request):

    BBA2=Attendance.objects.filter(courseandyear='BBA2')

    return render(request, "attendance/markclassattendancesub6.html",{"bba2":BBA2})

def markclassattendancesub6bba3(request):

    BBA3=Attendance.objects.filter(courseandyear='BBA3')

    return render(request, "attendance/markclassattendancesub6.html",{"bba3":BBA3})



def markclassattendancesub7bca1(request):

    BCA1=Attendance.objects.filter(courseandyear='BCA1')

    return render(request, "attendance/markclassattendancesub7.html",{"bca1":BCA1})

def markclassattendancesub7bca2(request):

    BCA2=Attendance.objects.filter(courseandyear='BCA2')

    return render(request, "attendance/markclassattendancesub7.html",{"bca2":BCA2})

def markclassattendancesub7bca3(request):

    BCA3=Attendance.objects.filter(courseandyear='BCA3')

    return render(request, "attendance/markclassattendancesub7.html",{"bca3":BCA3})

def markclassattendancesub7bcom1(request):

    BCOM1=Attendance.objects.filter(courseandyear='BCOM1')

    return render(request, "attendance/markclassattendancesub7.html",{"bcom1":BCOM1})

def markclassattendancesub7bcom2(request):

    BCOM2=Attendance.objects.filter(courseandyear='BCOM2')

    return render(request, "attendance/markclassattendancesub7.html",{"bcom2":BCOM2})

def markclassattendancesub7bcom3(request):

    BCOM3=Attendance.objects.filter(courseandyear='BCOM3')

    return render(request, "attendance/markclassattendancesub7.html",{"bcom3":BCOM3})

def markclassattendancesub7bba1(request):

    BBA1=Attendance.objects.filter(courseandyear='BBA1')

    return render(request, "attendance/markclassattendancesub7.html",{"bba1":BBA1})

def markclassattendancesub7bba2(request):

    BBA2=Attendance.objects.filter(courseandyear='BBA2')

    return render(request, "attendance/markclassattendancesub7.html",{"bba2":BBA2})

def markclassattendancesub7bba3(request):

    BBA3=Attendance.objects.filter(courseandyear='BBA3')

    return render(request, "attendance/markclassattendancesub7.html",{"bba3":BBA3})



def markclassattendancesub8bca1(request):

    BCA1=Attendance.objects.filter(courseandyear='BCA1')

    return render(request, "attendance/markclassattendancesub8.html",{"bca1":BCA1})

def markclassattendancesub8bca2(request):

    BCA2=Attendance.objects.filter(courseandyear='BCA2')

    return render(request, "attendance/markclassattendancesub8.html",{"bca2":BCA2})

def markclassattendancesub8bca3(request):

    BCA3=Attendance.objects.filter(courseandyear='BCA3')

    return render(request, "attendance/markclassattendancesub8.html",{"bca3":BCA3})

def markclassattendancesub8bcom1(request):

    BCOM1=Attendance.objects.filter(courseandyear='BCOM1')

    return render(request, "attendance/markclassattendancesub8.html",{"bcom1":BCOM1})

def markclassattendancesub8bcom2(request):

    BCOM2=Attendance.objects.filter(courseandyear='BCOM2')

    return render(request, "attendance/markclassattendancesub8.html",{"bcom2":BCOM2})

def markclassattendancesub8bcom3(request):

    BCOM3=Attendance.objects.filter(courseandyear='BCOM3')

    return render(request, "attendance/markclassattendancesub8.html",{"bcom3":BCOM3})

def markclassattendancesub8bba1(request):

    BBA1=Attendance.objects.filter(courseandyear='BBA1')

    return render(request, "attendance/markclassattendancesub8.html",{"bba1":BBA1})

def markclassattendancesub8bba2(request):

    BBA2=Attendance.objects.filter(courseandyear='BBA2')

    return render(request, "attendance/markclassattendancesub8.html",{"bba2":BBA2})

def markclassattendancesub8bba3(request):

    BBA3=Attendance.objects.filter(courseandyear='BBA3')

    return render(request, "attendance/markclassattendancesub8.html",{"bba3":BBA3})




def regbox(request):

    s=Attendance.objects.all()
    if request.method == "POST":
    
     rno = request.POST.get("box")
     match = Attendance.objects.filter(regnum=rno)     
    
     return render(request, "attendance/regbox.html", {"match1":match, "alldata":s})
    else:
    
       nomatch=Attendance.objects.all()
    return render(request, "attendance/regbox.html", {"nomatch1":nomatch, "alldata":s})


def viewrec(request):
      s=Records.objects.all()
      return render(request, "attendance/viewrec.html", {"allstudents": s})


def datewiserec(request):
    s=Records.objects.all()
    if request.method == "POST":
    
     dt = request.POST.get("box")
     core = request.POST.get("box2")
     match = Records.objects.filter(copydate=dt, copycourse=core)
    
     return render(request, "attendance/datewiserec.html", {"match1":match, "alldata":s})
    else:
    
       nomatch=Records.objects.all()
    return render(request, "attendance/datewiserec.html", {"nomatch1":nomatch, "alldata":s})


def studentrec(request):
    s=Records.objects.all()
    if request.method == "POST":
    
     rno = request.POST.get("box")
     match = Records.objects.filter(copyregnum=rno)     
    
     return render(request, "attendance/studentrec.html", {"match1":match, "alldata":s})
    else:
    
       nomatch=Records.objects.all()
    return render(request, "attendance/studentrec.html", {"nomatch1":nomatch, "alldata":s})



def myrec(request):
    s=Records.objects.all()
    if request.method == "POST":
    
     rno = request.POST.get("box")
     match = Records.objects.filter(copyregnum=rno)     
    
     return render(request, "attendance/myrec.html", {"match1":match, "alldata":s})
    else:
    
       nomatch=Records.objects.all()
    return render(request, "attendance/myrec.html", {"nomatch1":nomatch, "alldata":s})


def deleterec(request, id):
    
    s= Records.objects.get(pk=id)
    s.delete()
    return redirect('viewrec')

def home(request):
      return render(request, "attendance/home.html")
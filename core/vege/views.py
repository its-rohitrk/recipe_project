from django.shortcuts import render,redirect
from .models import *

#from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Sum
import re
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.
@login_required(login_url="/login_page/")
def recepies(request):

    if request.method=="POST":
        data = request.POST
        receipe_name = data.get('receipe_name')
        receipe_description = data.get("receipe_description")
        receipe_img = request.FILES["receipe_img"]

        Receipe.objects.create(
            receipe_name =receipe_name,
            receipe_description =receipe_description,
            receipe_img = receipe_img
        )
        return redirect('/a1/')

    queryset = Receipe.objects.all()

    if request.GET.get("search"):

        queryset = queryset.filter(receipe_name__icontains = request.GET.get("search"))

    context = {"recepies":queryset}
        #print(receipe_name,receipe_description,receipe_img)
    return render(request,'recepies.html',context)

@login_required(login_url="/login_page/")
def delete_recepie(request,id):
    queryset = Receipe.objects.get(id=id)
    queryset.delete()
    return redirect('/a1/')


@login_required(login_url="/login_page/")
def update_recepie(request,id):
    queryset = Receipe.objects.get(id=id)
    context = {"recepie":queryset}
    if request.method=="POST":
        data = request.POST

        receipe_name = data.get('receipe_name')
        receipe_description = data.get("receipe_description")

        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description
        try:
            receipe_img = request.FILES["receipe_img"]

            if receipe_img:
                queryset.receipe_img = receipe_img
        except:
            pass
        queryset.save()
        return redirect('/a1/')

    return render(request,"update_recepie.html",context)



# def register(request):
#     if request.method=="POST":
#         first_name = request.POST.get("first_name")
#         last_name = request.POST.get("last_name")
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#
#         user = User.objects.filter(username=username)
#         if user.exists():
#             messages.error(request, "Username already taken.")
#             return redirect("/register")
#
#
#         user = User.objects.create(
#             first_name=first_name,
#             last_name = last_name,
#             username = username
#             )
#         user.set_password(password)
#         user.save()
#         messages.success(request, "Account created successfully.")
#         return redirect("/register/")
#
#     return render(request,"register.html")


def is_valid_username(username):
    return len(username) >= 5

def is_valid_password(password):
    # Password should be at least 8 characters long and contain at least one alphanumeric character and one special character
    return len(password) >= 5

def  register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Validate username length
        if not is_valid_username(username):
            messages.error(request, "Username must be at least 5 characters long.")
            return redirect("/register")

        # Validate password length and character requirements
        if not is_valid_password(password):
            messages.error(request,
                           "Password must be at least 8 characters long and contain at least one alphanumeric character and one special character.")
            return redirect("/register")

        user = User.objects.filter(username=username)
        if user.exists():
            messages.error(request, "Username already taken.")
            return redirect("/register")

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone = phone,
            email=email


        )
        user.set_password(password)
        user.save()
        messages.success(request, "Account created successfully.")
        return redirect("/register/")

    return render(request, "register.html")


def login_page(request):
    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid user name")
            return redirect("/login_page/")
        user = authenticate(username=username,password=password)
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect("/login_page/")
        else:
            login(request,user)
            return redirect("/a1/")

    return render(request,"login.html")

@login_required(login_url="/login_page/")
def logout_page(request):
    logout(request)

    return redirect('/login_page')

@login_required(login_url="/login_page/")
def get_student(request):
    page_obj = Student.objects.all()

    # if request.GET.get("search"):
    #     search1 = request.GET.get("search")
    #     page_obj = page_obj.filter(student_name__icontains = search1)

    # paginator = Paginator(queryset,400)  # Show 25 contacts per page.
    #
    # page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number)
    # total_page = page_obj.paginator.num_pages


    return render(request,"student1.html",{"queryset":page_obj})

@login_required(login_url="/login_page/")
def see_marks(request, student_id):
    marks1 = SubjectMarks.objects.filter(student__student_id__student_id = student_id)
    print("##########",marks1)
    name=marks1[0].student

    print(name)
    total_marks = marks1.aggregate(total_marks = Sum('marks'))

    # rank = Student.objects.annotate(marks=Sum("studentmarks__marks")).odrer_by('-marks',"-student_age")
    # print(rank)
    return render(request,"marks.html",{"marks1":marks1,'total':total_marks['total_marks'],"name":name})

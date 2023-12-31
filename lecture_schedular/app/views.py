from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from .models import Instructor, Course, Lecture, Batch
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


def home(request):
    if request.user.is_authenticated and request.user.role == "Instructor":
        lectures = Lecture.objects.filter(instructor = request.user.id)
        return render(request, "index.html", {"lectures": lectures})
    else:
        lectures = Lecture.objects.all()
        return render(request, "index.html", {"lectures": lectures})



def sign_in(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            print(user)
            login(request, user)
            return redirect("home")
        

    return render(request, "login.html")


def signout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('sign_in') 

    
@login_required(login_url="sign_in")
def list_instructors(request):
    
    if request.method == "GET":
        instructors = Instructor.objects.all().exclude(role ="Admin")
        batches = Batch.objects.all()

    elif request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        password = email.split("@")[0] + "@1234"

        Instructor.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            contact=contact,
            password=password,
            role = "Instructor"
        )
        return redirect("instructors")

    context = {
        'instructors': instructors,
        'batches': batches,
    }
    return render(request, 'list_instructors.html', context)

def add_course(request):
    instructors = Instructor.objects.all()
    courses = Course.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        level = request.POST.get('level')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        course = Course.objects.create(
            name=name,
            level=level,
            description=description,
            image=image
        )

        return redirect('add_course')

    return render(request, 'add_course.html', {"instructors": instructors, "courses": courses})

def add_batch(request):
    if request.method == "POST":
        course_id = request.POST.get("course_id")
        batch_name = request.POST.get("batch_name")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        course = Course.objects.get(pk=course_id)

        new_batch = Batch.objects.create(
            course=course,
            batch_name=batch_name,
            start_date=start_date,
            end_date=end_date,
        )

        messages.success(request, "Batch added successfully.")
        return redirect('add_course')



def assign_lecture(request):
    if request.method == 'POST':
        instructor_id = request.POST.get('instructor_id')
        date = request.POST.get('date')
        batch_id = request.POST.get("batch_id")
        batch = Batch.objects.get(id=batch_id)

        if Lecture.objects.filter(instructor_id=instructor_id, date=date).exists():
            messages.error(request, "Lecture clash! This instructor already has a lecture scheduled on the selected date")
            return redirect("instructors")

        Lecture.objects.create(
            instructor_id=instructor_id,
            batch=batch,
            date=date
        )

        return redirect('instructors')

    instructors = Instructor.objects.all()
    return render(request, 'assign_lecture.html', {'instructors': instructors})

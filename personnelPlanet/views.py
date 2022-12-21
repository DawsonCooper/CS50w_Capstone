from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django import forms
from .models import User, Availability, Schedule, Company, EmployeeTracker, Messages
from phonenumber_field.formfields import PhoneNumberField
from random import randrange, randint

# Create your views here.


class RegisterForm(forms.Form):
    firstName = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'First Name'}), required=False, max_length=25)
    lastName = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Last Name'}), required=False, max_length=25)
    phoneNumber = PhoneNumberField(widget=forms.TextInput(
        attrs={'placeholder': 'Phone Number'}), region="US", required=False, max_length=25)
    isEmployer = forms.BooleanField(required=False)
    company = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Company Name'}), required=False, max_length=25)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}), max_length=32, required=False)


class LoginForm(forms.Form):
    workId = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Work Id'}), required=True
    )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}), required=True
    )


@csrf_exempt
def availability(request):
    # In post req we will be getting a users avail as a json obj {day: shift}
    # we will want to loop over that obj and populate the avail model with userId, day, shift in each iteration
    data = json.loads(request.body)
    availObj = data.get('body')
    print(request.user)
    employee = User.objects.filter(workId=request.user).values('pk')
    print(employee[0]['pk'])

    for day in availObj:

        try:
            check = Availability.objects.get(
                employee=employee[0]['pk'], day=day)
            print(check)

        except:
            newAvail = Availability(
                employee=employee,
                day=day,
                shift=availObj[day]
            )
            newAvail.save()
        if (check):
            Availability.objects.filter(
                employee=employee[0]['pk'], day=day).update(shift=availObj[day])
    return JsonResponse({
        'message': 'success'
    })


@csrf_exempt
def schedules(request, workerId):
    print(workerId)
    schedule = Schedule.objects.filter(employee=workerId)
    print(schedule)
    schedule = schedule[0].serialize()
    print(schedule)
    return JsonResponse({
        'schedule': schedule
    })


def home(request):
    # User information (company, shifts,)
    user = request.user
    print(user)
    user = User.objects.filter(username=user)

    return render(request, 'home.html')


def hire(request):
    # Only for employers allow employer to link a user with their company and enter in employee information (pay, position, etc)
    # link employee using employee id that should be auto generated
    return render(request, 'hire.html')


def shift(request):
    # for employee (a grid like page with day and shift information, swap shift functionality, call in functionality)
    # for emplyer (input fields for adding/removing shift information, swap shift approval call in notices)
    if request.user.isEmployer:
        workerList = User.objects.filter(
            company=request.user.company).values()
        workers = workerList.values('id', 'workId')
        schedules = []
        for employee in workers:
            if Schedule.objects.filter(employee=employee['id']).values():
                schedules.append(Schedule.objects.filter(
                    employee=employee['id']).values())

        print(schedules, workers)
        return render(request, 'employer/shift.html', {
            'schedules': schedules,
            'workers': workers,
        })
    else:

        employeeId = request.user.id
        schedule = Schedule.objects.filter(employee=employeeId).values()
        schedule = schedule[0]
        for day in schedule:
            print(day)
            if not isinstance(schedule[day], int):
                if len(schedule[day]) > 3:
                    print(schedule[day])
                    schedule[day] = schedule[day].split('-')
                    print(day)

        print(schedule)
        return render(request, 'shift.html', {
            'schedule': schedule
        })


def profile(request):
    # More specific user info (company id, pay, hours worked, position, etc)

    return render(request, 'profile.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data["workId"]
            password = form.cleaned_data["password"]
            print(username, password, request)
            user = User.objects.get(workId=username, password=password)

            print(user)
            if user is not None:
                login(request, user)
                return render(request, 'home.html', {
                })
        else:
            return render(request, "login.html", {
                "message": "Invalid work Id and/or password."
            })

    return render(request, 'login.html', {
        'loginForm': LoginForm
    })


def register(request):
    # simple registration for employees
    # for employer they should be able to register a company
    if request.method == "POST":

        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data["firstName"]
            last_name = form.cleaned_data["lastName"]
            phoneNumber = form.cleaned_data["phoneNumber"]
            isEmployer = form.cleaned_data["isEmployer"]
            company = form.cleaned_data["company"]
            password = form.cleaned_data["password"]
        # generate username (make sure to display it to the user) and create new user
            fInital = first_name[0]
            lInital = last_name[0]
            oneDigit = randint(0, 9)
            threeDigit = randrange(100, 999)
            workId = f"{fInital}{oneDigit}{lInital}{oneDigit}{threeDigit}"
            createUser = User(
                username=workId,
                first_name=first_name,
                last_name=last_name,
                workId=workId,
                phoneNumber=phoneNumber,
                isEmployer=isEmployer,
                company=company,
                password=password
            )
            createUser.save()
            print(workId)
            login(request, createUser)
            return home(request)

        else:
            for field in form:
                print("Field Error:", field.name,  field.errors)
            print(form.errors.as_data())
            return render(request, "register.html", {
                'regForm': RegisterForm,
            })

    return render(request, "register.html", {
        'regForm': RegisterForm,
    })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

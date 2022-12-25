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
from .models import User, Availability, Schedule, Company, EmployeeTracker, Messages, Memo, Clock
from phonenumber_field.formfields import PhoneNumberField
from random import randrange, randint
import datetime
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


DAYS = ["monday", "tuesday", "wednesday",
        "thursday", "friday", "saturday", "sunday"]


@csrf_exempt
def clock(request):
    employee = request.user.id
    if request.method == 'POST':
        day = datetime.date.today()
        day = datetime.datetime(day.year, day.month, day.day).weekday()
        day = DAYS[day]
        try:
            Clock.objects.get(employee=employee)
            return JsonResponse({'message': 'failed to clock in'})
        except Clock.DoesNotExist:
            Clock.objects.create(employee=employee, day=day,
                                 clockIn=datetime.datetime.now())
            return JsonResponse({
                'message': 'clocked in'
            })
    elif request.method == 'PUT':
        now = datetime.datetime.now()
        print(now, employee)
        try:
            clockStatus = Clock.objects.get(employee=employee)
            clockIn = clockStatus.clockIn
            clockIn = datetime.datetime(
                clockIn.year, clockIn.month, clockIn.day, clockIn.hour, clockIn.minute, clockIn.second)
            worked = now - clockIn
            hoursWorked = round(worked.total_seconds() / 60 / 60, 2)
            print(hoursWorked)
            employeeInstace = User.objects.get(id=employee)
            employeeInstace.hoursWorked = employeeInstace.hoursWorked + hoursWorked
            employeeInstace.save()
            clockStatus.delete()

        except Clock.DoesNotExist:
            return JsonResponse({'message': 'Failed to clock out: You are not clocked in'})

    return JsonResponse({
        'message': 'Clock status failed'
    })


@csrf_exempt
def memo(request):
    # put is for removing the memo
    if request.method == 'PUT':
        data = json.loads(request.body)
        memoId = data.get('memoId')
        Memo.objects.filter(id=memoId).delete()
        return JsonResponse({'message': 'Memo removed'})
    elif request.method == 'POST':
        data = json.loads(request.body)
        subject = data.get('subject')
        body = data.get('body')
        company = request.user.company
        print(subject, body, company)
        Memo.objects.create(subject=subject, body=body, company=company)
    return JsonResponse({'message': 'Missed request'})


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
    try:
        schedule = schedule[0].serialize()
    except IndexError:
        return JsonResponse({
            'schedule': {
                'employee': workerId,
                'monday': 'off-off',
                'tuesday': 'off-off',
                'wednesday': 'off-off',
                'thursday': 'off-off',
                'friday': 'off-off',
                'saturday': 'off-off',
                'sunday': 'off-off',
            }
        })

    print(schedule)
    return JsonResponse({
        'schedule': schedule
    })


@login_required(login_url='/login')
def home(request):
    # User information (company, shifts,)
    user = request.user
    user = User.objects.filter(username=user).values()
    memos = Memo.objects.filter(company=user[0]['company']).values()
    context = {'user': user, 'memos': memos}
    try:
        clockStat = Clock.objects.get(employee=request.user.id)
        clockIn = clockStat.clockIn
        clockIn = datetime.datetime(
            clockIn.year, clockIn.month, clockIn.day, clockIn.hour, clockIn.minute, clockIn.second)
        now = datetime.datetime.now()
        worked = now - clockIn
        hoursToday = round(worked.total_seconds() / 60 / 60, 2)
        context['hoursToday'] = hoursToday
    except Clock.DoesNotExist:
        pass
    day = datetime.date.today()
    day = datetime.datetime(day.year, day.month, day.day).weekday()
    day = DAYS[day]
    try:
        shift = Schedule.objects.filter(
            employee=request.user.id).values(day)
        shift = shift[0][day]
        if shift == "off-off":
            shift = 'off'

    except Exception:
        shift = "No schedule"
    context['shift'] = shift
    return render(request, 'home.html', {
        'context': context,
        'counter': range(1, len(memos) + 1),
    })


def hire(request):
    # Only for employers allow employer to link a user with their company and enter in employee information (pay, position, etc)
    # link employee using employee id that should be auto generated
    return render(request, 'hire.html')


@csrf_exempt
def shift(request):
    # for employee (a grid like page with day and shift information, swap shift functionality, call in functionality)
    # for emplyer (input fields for adding/removing shift information, swap shift approval call in notices)
    if request.method == 'POST':
        data = json.loads(request.body)
        scheduleChanges = data.get('schedule')
        workerId = data.get('workerId')
        print('working')
        print(scheduleChanges, workerId)
        try:
            exists = Schedule.objects.get(employee=workerId)
            exists.update(
                monday=scheduleChanges[0],
                tuesday=scheduleChanges[1],
                wednesday=scheduleChanges[2],
                thursday=scheduleChanges[3],
                friday=scheduleChanges[4],
                saturday=scheduleChanges[5],
                sunday=scheduleChanges[6],
            )
            print('updating')
        except Schedule.DoesNotExist:
            change = Schedule(
                employee=workerId,
                monday=scheduleChanges[0],
                tuesday=scheduleChanges[1],
                wednesday=scheduleChanges[2],
                thursday=scheduleChanges[3],
                friday=scheduleChanges[4],
                saturday=scheduleChanges[5],
                sunday=scheduleChanges[6],
            )
            change.save()
            print('creating')
        return JsonResponse({
            'message': 'Shift changed successfully'
        })
    if request.user.isEmployer and request.method == 'GET':
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

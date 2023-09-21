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
from .models import User, Availability, Schedule, Company, EmployeeTracker, Messages, Memo, Clock, Tasks
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
def get_schedule_by_week(request, week, workerId):
    print(week)

    try:
        schedule = Schedule.objects.filter(
            week=week).filter(employee=workerId)
        print(schedule)
    except Exception as e:
        print(e)
        return JsonResponse({'errors': 'Employee schedule not found'})
    try:
        schedule = schedule[0].serialize()
        return JsonResponse({'schedule': schedule})
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


@csrf_exempt
def addToTask(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        task = Tasks.objects.filter(data.get('taskId')).values()
        print(task)
        current = task['assignedTo']
        new = f'{current} {request.user.workId}'
        print(new)
        Tasks.objects.filter(data.get('taskId')).update(assignedTo=new)
        print('----------------------------')


@csrf_exempt
def task(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        empId = 0
        print(data.get('assignTo'))
        if len(data.get('assignTo')) == 1:
            temp = data.get('assignTo')

            empId = User.objects.filter(
                workId=temp[0]).values('id')
            print(empId)
        try:
            Tasks.objects.create(assignedTo=data.get('assignTo'), taskBody=data.get('taskBody'), complete=data.get('status'),
                                 assingedBy=request.user.id, company=request.user.company, assignedToId=empId
                                 )
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'error: task unable to be created'})
        return JsonResponse({'message': 'Task creation complete'})

    if request.method == 'GET':
        # TODO: pull task info by company serialize and send to client
        taskList = Tasks.objects.filter(
            company=request.user.company).all()
        return JsonResponse({
            'taskList': [task.serialize() for task in taskList]
        })

    if request.method == 'PUT':
        data = json.loads(request.body)
        # TODO: handle status changes to tasks from employees and deletions from employers
        if data.get('status'):
            print(data.get('status'), data.get('taskId'))
            if request.user.isEmployer:
                try:
                    Tasks.objects.filter(id=data.get('taskId')).delete()
                    return JsonResponse({'status': 'Task successfully removed'})
                except Exception as e:
                    return JsonResponse({'status': f'Your task deletion failed with code: {e}'})
            else:
                Tasks.objects.filter(pk=data.get('taskId')).update(
                    complete=data.get('status'))
                return JsonResponse({'status': 'Task marked as complete'})


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
            employeeInstace.hoursWorked = round(
                employeeInstace.hoursWorked + hoursWorked, 2)
            employeeInstace.save()
            clockStatus.delete()

        except Clock.DoesNotExist:
            return JsonResponse({'message': 'Failed to clock out: You are not clocked in'})

    return JsonResponse({
        'message': 'Clock status failed'
    })


@csrf_exempt
def empInfo(request, empId):
    if request.method == 'GET':
        emp = User.objects.get(id=empId)
        emp = emp.serialize()
        return JsonResponse({
            'employee': emp,
        })
    if request.method == 'PUT':
        data = json.loads(request.body)
        print(data)
        if data['terminate'] == True:
            try:
                User.objects.filter(id=empId).delete()
                Messages.objects.filter(fromUserId=empId).all().delete()
                Tasks.objects.filter(assignedToId=empId).all().delete()
                Clock.objects.filter(employee=empId).all().delete()
                Availability.objects.filter(employee=empId).all().delete()
                Schedule.objects.filter(employee=empId).all().delete()
                return JsonResponse({'message': 'Succesfully terminated employee'})
            except Exception:
                return JsonResponse({'message': 'An error occurred while trying to remove the employee please check your employee list and try again.'})
        try:
            User.objects.filter(id=empId).update(
                workId=data['workId'], payRate=data['payRate'], company=data['company'])

        except User.DoesNotExist:
            return JsonResponse({
                'Error': 'User does not exist'
            })
        except Exception as err:
            return JsonResponse({
                'Error': err
            })
        return JsonResponse({
            'message': 'Changes completed'
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


def get_availability(request, user):
    # use user to get the corrisponding availability
    existingAvail = Availability.objects.filter(employee=user).all().values()
    availArr = []
    for avail in existingAvail:
        if avail['shift']:
            temp = avail['shift'] + '-' + avail['day']
            availArr.append(temp)
    print('get', availArr)
    # return availability
    return JsonResponse({'availability': availArr})


@csrf_exempt
def availability(request):
    # In post req we will be getting a users avail as a json obj {day: shift}
    # we will want to loop over that obj and populate the avail model with userId, day, shift in each iteration
    data = json.loads(request.body)
    availObj = data.get('body')
    print(request.user)
    employee = User.objects.filter(workId=request.user.workId).values('pk')

    for day in availObj:

        try:
            Availability.objects.get(
                employee=employee[0]['pk'], day=day)
            Availability.objects.filter(
                employee=employee[0]['pk'], day=day).update(shift=availObj[day])

        except Availability.DoesNotExist:
            newAvail = Availability(
                employee=employee,
                day=day,
                shift=availObj[day]
            )
            newAvail.save()

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

    memos = Memo.objects.filter(company=user.company).values()
    context = {'user': user, 'memos': memos}
    todayDT = datetime.datetime.now()
    today = User.objects.filter(workId=user.workId).values('hoursWorked')
    if todayDT.strftime('%a') == 'Mon':
        hours = User.objects.filter(workId=user.workId).values(
            'hoursWorked', 'totalHours')
        totalHours = 0
        for item in hours:
            totalHours = item['hoursWorked'] + totalHours
        User.objects.filter(workId=request.user.workId).update(
            totalHours=totalHours)
        User.objects.update(hoursWorked=0)
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

    try:
        messages = Messages.objects.filter(
            company=request.user.company).values()
        messages = messages.order_by('-timestamp').all()

        context['messages'] = messages
    except Messages.DoesNotExist:
        context['messages'] = 'No company messages'

    return render(request, 'home.html', {
        'context': context,
        'counter': range(1, len(memos) + 1),
    })


@csrf_exempt
@login_required(login_url='/login')
def messages(request):
    context = {}
    if request.method == 'GET':
        try:
            messages = Messages.objects.filter(
                company=request.user.company).all().values()

            context['messages'] = messages
        except Messages.DoesNotExist:
            context['messages'] = 'No company messages'

        return render(request, 'messages.html', {
            'context': context
        })
    if request.method == 'POST':
        # when we send a fetch we will want to send message body and thats it
        # we can autogen timestamp and get user from request struct
        data = json.loads(request.body)
        message = data.get('body')
        Messages.objects.create(
            fromUser=request.user.first_name,
            fromUserId=request.user.id,
            company=request.user.company,
            content=message,
        )
        return JsonResponse({'message': 'Message Sent!'})
    return JsonResponse({'message': 'Failed to send message'})


@csrf_exempt
@login_required(login_url='/login')
def shift(request):
    # for employee (a grid like page with day and shift information, swap shift functionality, call in functionality)
    # for emplyer (input fields for adding/removing shift information, swap shift approval call in notices)
    if request.method == 'POST':
        data = json.loads(request.body)
        scheduleChanges = data.get('schedule')
        workerId = data.get('workerId')
        week = data.get('week')
        print('working')
        print(scheduleChanges, workerId)
        # VERY POOR PRACTICE USING ARRAY INSTEAD OF OBJECT THESE INDEXS ARE ARBITRARY

        Schedule.objects.update_or_create(
            employee=workerId,
            week=week,
            defaults={
                'monday': scheduleChanges[0],
                'tuesday': scheduleChanges[1],
                'wednesday': scheduleChanges[2],
                'thursday': scheduleChanges[3],
                'friday': scheduleChanges[4],
                'saturday': scheduleChanges[5],
                'sunday': scheduleChanges[6],
            })
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
        try:
            schedule = Schedule.objects.filter(employee=employeeId)
            print(schedule)
        except Schedule.DoesNotExist:
            Schedule.objects.create(employee=request.user.id)
        schedule = Schedule.objects.filter(employee=employeeId).values()
        schedule = schedule[0]
        for day in schedule:
            if not isinstance(schedule[day], int):
                if len(schedule[day]) > 3 and len(schedule[day]) < 10:
                    schedule[day] = schedule[day].split('-')

        print(schedule)
        return render(request, 'shift.html', {
            'schedule': schedule
        })


@login_required(login_url='/login')
def profile(request):
    # More specific user info (company id, pay, hours worked, position, etc)
    context = {}
    if request.method == 'POST':
        # ADD CONDITIONS TO UPDATE EACH INPUT IF IT HAS A VALUE
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['firstName']:
                first_name = form.cleaned_data["firstName"]
                try:
                    User.objects.filter(id=request.user.id).update(
                        first_name=first_name)
                except User.DoesNotExist:
                    context['error'] = 'Problem locating your profile infomation please try again'
            if form.cleaned_data['lastName']:
                last_name = form.cleaned_data["lastName"]
                try:
                    User.objects.filter(id=request.user.id).update(
                        last_name=last_name)
                except User.DoesNotExist:
                    context['error'] = 'Problem locating your profile infomation please try again'
            if form.cleaned_data['phoneNumber']:
                phoneNumber = form.cleaned_data["phoneNumber"]
                try:
                    User.objects.filter(id=request.user.id).update(
                        phoneNumber=phoneNumber)
                except User.DoesNotExist:
                    context['error'] = 'Problem locating your profile infomation please try again'

    empList = User.objects.filter(
        company=request.user.company).all().values("id", "first_name", "last_name", 'workId', 'isEmployer')
    print(empList)
    if empList:
        context['employees'] = empList

    context['form'] = RegisterForm
    return render(request, 'profile.html', {
        'context': context})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data["workId"]
            password = form.cleaned_data["password"]
            print(username, password, request)
            try:
                User.objects.get(workId=username, password=password)
                user = User.objects.get(workId=username, password=password)
            except User.DoesNotExist:
                user = None
            print(user)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, "login.html", {
                'loginForm': LoginForm,
                "message": "Invalid work Id and/or password."
            })

    return render(request, 'login.html', {
        'loginForm': LoginForm,
        'message': False
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
            return profile(request)

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

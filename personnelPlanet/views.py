from django.shortcuts import render

# Create your views here.


def home(request):
    # User information (company, shifts,)
    return render(request, 'home.html')


def hire(request):
    # Only for employers allow employer to link a user with their company and enter in employee information (pay, position, etc)
    # link employee using employee id that should be auto generated
    return render(request, 'hire.html')


def shift(request):
    # for employee (a grid like page with day and shift information, swap shift functionality, call in functionality)
    # for emplyer (input fields for adding/removing shift information, swap shift approval call in notices)
    return render(request, 'shift.html')


def profile(request):
    # More specific user info (company id, pay, hours worked, position, etc)

    return render(request, 'profile.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    # simple registration for employees
    # for employer they should be able to register a company
    return render(request, 'register.html')


def logout(request):
    return render(request, 'logout.html')

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
from .models import User, Availability, Shifts, Company, EmployeeTracker, Messages
from phonenumber_field.formfields import PhoneNumberField

# Create your views here.


class RegisterForm(forms.Form):
    firstName = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'First Name'}), required=True)
    lastName = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Last Name'}), required=True)
    phoneNumber = PhoneNumberField(widget=forms.TextInput(
        attrs={'placeholder': 'Phone Number'}), required=True)
    is_employer = forms.BooleanField()
    company = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Company Name'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}), max_length=32)


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Username'}), required=True
    )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}), required=True
    )


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
    return render(request, 'login.html', {
        'form': LoginForm
    })


def register(request):
    # simple registration for employees
    # for employer they should be able to register a company
    if request.method == "POST":

        form = RegisterForm(request.POST)
        if form.is_valid():
            firstName = form.cleaned_data["FirstName"]
            lastName = form.cleaned_data["LastName"]
            password = form.cleaned_data["Password"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match.",
                'form': RegisterForm,
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username, password)
            user.save()
            User.objects.filter(username=username).update(
                bio=bio, name=name)
            print(bio, name)
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken.",
                'postForm': PostForm,
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html", {
            'postForm': PostForm,
        })
    return render(request, 'register.html', {'form': RegisterForm})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

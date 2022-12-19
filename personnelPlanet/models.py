from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class Company(models.Model):
    companyName = models.CharField(max_length=20, default="", blank=True)
    employeeCount = models.IntegerField(null=True)


class User(AbstractUser):
    workId = models.CharField(max_length=10, default='000000')
    phoneNumber = PhoneNumberField(default='(555) 555 5555')
    payRate = models.FloatField(default=7.45)
    isEmployer = models.BooleanField(default=False)
    hoursWorked = models.IntegerField(default=0)
    company = models.CharField(max_length=25, null=True)


class Availability(models.Model):
    employee = models.IntegerField()
    day = models.CharField(max_length=10)
    # shift will be morning, evenning, or all
    shift = models.CharField(max_length=10, default='All')


class Shifts(models.Model):
    employee = models.IntegerField()
    day = models.CharField(max_length=10)
    start = models.TimeField(null=False, blank=False)
    end = models.TimeField(null=False, blank=False)


class EmployeeTracker(models.Model):
    company = models.IntegerField()
    employee = models.IntegerField()


class Messages(models.Model):
    fromUser = models.IntegerField(blank=False, null=False)
    toUser = models.IntegerField(blank=False, null=False)
    content = models.CharField(max_length=350, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

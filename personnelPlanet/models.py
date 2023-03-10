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
    hoursWorked = models.FloatField(default=0)
    company = models.CharField(max_length=25, null=True)
    totalHours = models.IntegerField(null=True, default=0)

    def serialize(self):
        return {
            'workId': self.workId,
            'payRate': self.payRate,
            'isEmployer': self.isEmployer,
            'hoursWorked': self.hoursWorked,
            'company': self.company,
            'totalHours': self.totalHours
        }


class Availability(models.Model):
    employee = models.IntegerField()
    day = models.CharField(max_length=12)
    # shift will be morning, evenning, or all
    shift = models.CharField(max_length=10, default='None')


class Schedule(models.Model):
    employee = models.IntegerField()
    week = models.CharField(default='null', max_length=55)
    monday = models.CharField(default='off-off', max_length=15)
    tuesday = models.CharField(default='off-off', max_length=15)
    wednesday = models.CharField(default='off-off', max_length=15)
    thursday = models.CharField(default='off-off', max_length=15)
    friday = models.CharField(default='off-off', max_length=15)
    saturday = models.CharField(default='off-off', max_length=15)
    sunday = models.CharField(default='off-off', max_length=15)

    def serialize(self):
        return {
            'employee': self.employee,
            'week': self.week,
            'monday': self.monday,
            'tuesday': self.tuesday,
            'wednesday': self.wednesday,
            'thursday': self.thursday,
            'friday': self.friday,
            'saturday': self.saturday,
            'sunday': self.sunday
        }


class Clock(models.Model):
    employee = models.IntegerField()
    day = models.CharField(max_length=12)
    clockIn = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    clockOut = models.DateTimeField(auto_now_add=False, blank=True, null=True)


class EmployeeTracker(models.Model):
    company = models.IntegerField()
    employee = models.IntegerField()


class Messages(models.Model):
    fromUser = models.CharField(max_length=25, blank=False, null=False)
    fromUserId = models.IntegerField(default=0)
    company = models.CharField(max_length=25, blank=False, null=False)
    content = models.CharField(max_length=350, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class Memo(models.Model):
    subject = models.CharField(max_length=50)
    body = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    company = models.CharField(max_length=20, default='NA')


class Tasks(models.Model):
    assignedToId = models.IntegerField(default=0, blank=False, null=False)
    assignedTo = models.CharField(max_length=150, default='Team')
    taskBody = models.CharField(max_length=300, default='Task')
    complete = models.BooleanField(default=False)
    assingedBy = models.IntegerField(default=0)
    company = models.CharField(max_length=25, default='Company')

    def serialize(self):
        return {
            'id': self.pk,
            'assignedTo': self.assignedTo,
            'taskBody': self.taskBody,
            'complete': self.complete,
            'assingedBy': self.assingedBy,
        }

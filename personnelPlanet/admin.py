from django.contrib import admin
from .models import User, Availability, Schedule, Company, EmployeeTracker, Messages, Memo
# Register your models here.

admin.site.register(User)
admin.site.register(Availability)
admin.site.register(Schedule)
admin.site.register(Company)
admin.site.register(EmployeeTracker)
admin.site.register(Messages)
admin.site.register(Memo)

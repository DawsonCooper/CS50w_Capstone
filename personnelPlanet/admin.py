from django.contrib import admin
from .models import User, Availability, Shifts, Company, EmployeeTracker, Messages
# Register your models here.

admin.site.register(User)
admin.site.register(Availability)
admin.site.register(Shifts)
admin.site.register(Company)
admin.site.register(EmployeeTracker)
admin.site.register(Messages)

from django.contrib import admin

from .models import Employee, EmployeeType

admin.site.register(Employee)
admin.site.register(EmployeeType)
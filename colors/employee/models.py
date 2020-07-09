from django.db import models

class Employee(models.Model):
    employee_id = models.CharField(max_length=20, blank=False, primary_key=True)
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=13)
    door_no = models.IntegerField()
    street = models.CharField(max_length=35)
    area = models.CharField(max_length=20, default="")
    state = models.CharField(max_length=15)
    pincode = models.IntegerField()
    department = models.CharField(max_length=20)
    is_active_employee = models.CharField(max_length=5, default="YES")

    def __str__(self):
        return self.employee_id
    
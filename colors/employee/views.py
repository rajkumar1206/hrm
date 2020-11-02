from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail, EmailMessage
from .models import Employee, EmployeeType
from django.core import serializers
import json
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import requests
import string 
import random 
import sqlite3
import django
from django.conf import settings
from rest_framework.authtoken.models import Token
from leave.permissions import IsEmployee
  
# initializing size of random string  
N = 7


class index(APIView):
#     permission_classes = (IsAuthenticated, )
    def post(self, request):
        return Response({"data": "hi there, this is for demo trial"})


class employee_list(APIView):
    permission_classes = (IsAuthenticated & ~IsEmployee, )
    def get(self, request):
        try:
            data = serializers.serialize(
                "json", Employee.objects.filter(is_active_employee='YES'))
            json_data = {"status": "success", "data": json.loads(data)}
            return JsonResponse(json_data, safe=False)
        except:
            return JsonResponse({"status": "failed"})



class employee_id_list(APIView):
    permission_classes = (IsAuthenticated & ~IsEmployee, )
    def get(self, request):
        try:
            print("Employee List ids")
            data = serializers.serialize(
                "json", Employee.objects.filter(is_active_employee='YES'), fields=("employee_id", ))
            json_data = {"status": "success", "data": json.loads(data)}
            return JsonResponse(json_data, safe=False)
        except:
            return JsonResponse({"status": "failed"})


class employee_detail(APIView):
    permission_classes = (IsAuthenticated & ~IsEmployee, )
    def get(self, request,  employee_id):
        try:
            employee_detail = Employee.objects.get(employee_id=employee_id)
            employee_detail_dict = model_to_dict(employee_detail)
            json_data = {"status": "success", "data": employee_detail_dict}
            return JsonResponse(json_data, safe=False)
        except:
            err_data = {
                "status": "failed",
                "err_message": "Employee Doesn't exist with the given employee id"}
            return JsonResponse(err_data, safe=False)


class create_employee(APIView):
    permission_classes = (IsAuthenticated & ~IsEmployee, )
    def post(self, request):
        data = request.data["body"]["data"]
        try:
            # Random String producer
            random_pass = ''.join(random.choices(string.ascii_uppercase +
                                string.digits, k = N))

            print("Random password : "+str(random_pass))
            

            # creating user
            user =  User.objects.create_user(data["employee_id"], None, random_pass )
            user.save()

            # EMAIL NOTIFICCATION
            send_mail(
                'Your Employee ID and password',
                'Your username is : '+ data["employee_id"] + " \npassword : " + random_pass,
                settings.EMAIL_HOST_USER,
                [data["email"]],
                fail_silently=False,
            )

            # token creating for the user
            token = Token.objects.create(user=user)
            print(token.key)

            # Database Management
            emp_type = EmployeeType(employee_id=data["employee_id"], token=token.key, user_type="EMPLOYEE")
            emp_type.save()

            emp = Employee(employee_id=data["employee_id"], first_name=data["first_name"], middle_name=data["middle_name"], last_name=data["last_name"], email=data["email"], gender=data["gender"],
                                                                        date_of_birth=data["date_of_birth"], phone_number=int(data["phone_number"]), door_no=int(data["door_no"]), street=data["street"], area=data["area"], state=data["state"], pincode=int(data["pincode"]), department=data["department"])
            emp.save()
            return JsonResponse({"status": "success"})
        except django.db.utils.IntegrityError:
            return JsonResponse({"status": "failed", "err_message": "The employee id is already taken"})
        except ValueError:
            return JsonResponse({"status": "failed", "err_message": "Please enter valid credential"})
        except AttributeError:
            return JsonResponse({"status": "failed", "err_message": "Please enter the valid attribute credential"})
        except:
            return JsonResponse({"status": "failed", "err_message": "Some internal error"})




class delete_employee(APIView):
    permission_classes = (IsAuthenticated & ~IsEmployee, )
    def get(self, request, employee_id):
        try:
            total_update = Employee.objects.filter(employee_id=employee_id).update(
                is_active_employee='NO')
            if total_update == 0:
                return JsonResponse({"status": "failed"})
            else:    
                return JsonResponse({"status": "success"})
        except:
            return JsonResponse({"status": "failed"})



class update_employee(APIView):
    permission_classes = (IsAuthenticated & ~IsEmployee, )
    def post(self, request, employee_id):
        data = request.data["body"]["data"]
        try:
            if Employee.objects.filter(employee_id=employee_id).exists():
                qs = Employee.objects.get(employee_id=employee_id)
                dictionary_model = model_to_dict(qs)
                Employee.objects.filter(employee_id=employee_id).update(first_name=data["first_name"], middle_name=data["middle_name"], last_name=data["last_name"], email=data["email"], gender=data["gender"],
                                                                        date_of_birth=data["date_of_birth"], phone_number=int(data["phone_number"]), door_no=int(data["door_no"]), street=data["street"], area=data["area"], state=data["state"], pincode=int(data["pincode"]), department=data["department"])
                return JsonResponse({"status": "success"})
            else: 
                return JsonResponse({"status": "failed", "err_message": "Employee with the given Id doesn't exist"})
        except:
            return JsonResponse({"status": "failed", "err_message": "Server error"})

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Employee
from django.core import serializers
import json
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required

@api_view(['GET'])
@login_required
def employee_list(request):
    try:
        data = serializers.serialize(
            "json", Employee.objects.filter(is_active_employee='YES'))
        json_data = {"status": "success", "data": data}
        return JsonResponse(json_data, safe=False)
    except:
        return JsonResponse({"status": "failed"})


@api_view(['GET'])
@login_required
def employee_detail(request, employee_id):
    try:
        employee_detail = Employee.objects.get(employee_id=employee_id)
        employee_detail_dict = model_to_dict(employee_detail)
        return JsonResponse(employee_detail_dict, safe=False)
    except:
        err_data = {
            "status": "failed",
            "err_details": "Employee Doesn't exist with the given employee id"}
        return JsonResponse(err_data, safe=False)


@api_view(['POST'])
@login_required
def create_employee(request):
    print(request.data)
    data = request.data
    try:
        emp = Employee(employee_id=data.employee_id, first_name=data.first_name, middle_name=data.middle_name, last_name=data.last_name, email=data.email, gender=data.gender,
                    date_of_birth=data.date_of_birth, phone_number=data.phone_number, door_no=data.door_no, street=data.street, area=data.area, state=data.state, pincode=data.pincode, department=data.department)
        emp.save()
        return JsonResponse({"status": "success"})
    except:
        return JsonResponse({"status": "failed"})


@api_view(['GET'])
@login_required
def delete_employee(request, employee_id):
    try:
        Employee.objects.filter(employee_id=employee_id).update(
            is_active_employee='NO')
        return JsonResponse({"status": "success"})
    except:
        return JsonResponse({"status": "failed"})


@api_view(['POST'])
@login_required
def update_employee(request, employee_id):
    data = request.data
    try:
        Employee.objects.filter(employee_id=employee_id).update(first_name=data.first_name, middle_name=data.middle_name, last_name=data.last_name, email=data.email, gender=data.gender,
                                                                date_of_birth=data.date_of_birth, phone_number=data.phone_number, door_no=data.door_no, street=data.street, area=data.area, state=data.state, pincode=data.pincode, department=data.department)
        return JsonResponse({"status": "success"})
    except:
        return JsonResponse({"status": "failed"})

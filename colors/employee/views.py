from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Employee
from django.core import serializers
import json
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class index(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request):
        return Response({"data": "hi there, this is for demo trial"})


class employee_list(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        try:
            data = serializers.serialize(
                "json", Employee.objects.filter(is_active_employee='YES'))
            json_data = {"status": "success", "data": data}
            return JsonResponse(json_data, safe=False)
        except:
            return JsonResponse({"status": "failed"})



class employee_detail(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request,  employee_id):
        try:
            employee_detail = Employee.objects.get(employee_id=employee_id)
            employee_detail_dict = model_to_dict(employee_detail)
            json_data = {"status": "success", "data": employee_detail_dict}
            return JsonResponse(json_data, safe=False)
        except:
            err_data = {
                "status": "failed",
                "err_details": "Employee Doesn't exist with the given employee id"}
            return JsonResponse(err_data, safe=False)


class create_employee(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request):
        data = request.data["body"]["data"]
        try:
            emp = Employee(employee_id=data["employee_id"], first_name=data["first_name"], middle_name=data["middle_name"], last_name=data["last_name"], email=data["email"], gender=data["gender"],
                                                                        date_of_birth=data["date_of_birth"], phone_number=int(data["phone_number"]), door_no=int(data["door_no"]), street=data["street"], area=data["area"], state=data["state"], pincode=int(data["pincode"]), department=data["department"])
            emp.save()
            return JsonResponse({"status": "success"})
        except:
            return JsonResponse({"status": "failed"})



class delete_employee(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request, employee_id):
        print("YYY")
        print(employee_id)
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
    permission_classes = (IsAuthenticated, )
    def post(self, request, employee_id):
        data = request.data["body"]["data"]
        print(data)
        try:
            qs = Employee.objects.get(employee_id=employee_id)
            dic_model = model_to_dict(qs)
            if dic_model:
                Employee.objects.filter(employee_id=employee_id).update(first_name=data["first_name"], middle_name=data["middle_name"], last_name=data["last_name"], email=data["email"], gender=data["gender"],
                                                                        date_of_birth=data["date_of_birth"], phone_number=int(data["phone_number"]), door_no=int(data["door_no"]), street=data["street"], area=data["area"], state=data["state"], pincode=int(data["pincode"]), department=data["department"])
                return JsonResponse({"status": "success"})
            else: 
                return JsonResponse({"status": "failed"})
        except:
            return JsonResponse({"status": "failed"})

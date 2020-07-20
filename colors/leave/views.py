from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Leave, Application
from django.http import HttpResponse, JsonResponse
from slugify import slugify
from django.core import serializers
import json
import django
from .permissions import IsEmployee

from .models import Leave, Application


class create_leave(APIView):
    permission_classes = (IsAuthenticated & ~IsEmployee, )

    def post(self, request):
        try:
            data = request.data["body"]["data"]
            leave_form = Leave(leave_type=data["leave_type"], leave_slug=slugify(
                data["leave_type"]), leave_description=data["leave_description"], total_leaves_given=data["total_days"])
            leave_form.save()
            return JsonResponse({"status": "success"})
        except django.db.utils.IntegrityError:
            return JsonResponse({"status": "failed", "err_message": "Leave already exists"})


class leave_list(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        try:
            leave_list = serializers.serialize(
                "json", Leave.objects.all())
            return JsonResponse({"status": "success", "data": json.loads(leave_list)})
        except:
            return JsonResponse({"status": "failed", "err_message": "Unexpected error"})


class leave_types(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, leave_type):
        try:
            lea_appl_forms = Leave.objects.get(leave_slug=leave_type)
            total_forms = lea_appl_forms.application_set.all()
            leave_list = serializers.serialize(
                "json", total_forms.filter(approval="P"))
            return JsonResponse({"status": "success", "data": json.loads(leave_list)})
        except:
            return JsonResponse({"status": "failed", "err_message": "Unexpected error"})


class application_approval(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, pk):
        if request.data["body"]["data"] == "Approve":
            Application.objects.filter(pk=pk).update(approval="A")
        elif request.data["body"]["data"] == "Decline":
            Application.objects.filter(pk=pk).update(approval="R")
        return JsonResponse({"status": "success"})


class employee_records(APIView):
    permission_classes = [IsEmployee]

    def get(self, request, employee_id):
        try:
            record_list = serializers.serialize(
                'json', Application.objects.filter(employee_id=employee_id))
            return JsonResponse({"status": "success", "data": json.loads(record_list)})
        except:
            return JsonResponse({"status": "failed", "err_message": "Unexpected error"})


class leave_application(APIView):
    permission_classes = [IsEmployee]
    def post(self, request, employee_id, leave_type):
        try:
            data = request.data["body"]["data"]
            leave_object = Leave.objects.filter(leave_slug=leave_type).first()
            appl = leave_object.application_set.create(employee_id=employee_id, email=data["email"], leave_type=data["leave"], start_date=data["start_date"], end_date=data["end_date"], remark=data["remark"], approval="P")
            appl.save()
            return JsonResponse({"status": "success"}) 
        except:
            return JsonResponse({"status": "failed"})

        

class employee_leave_details(APIView):
    def get(self, request, employee_id):
        pass

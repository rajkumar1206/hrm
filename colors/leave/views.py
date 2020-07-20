from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Leave, Application
from django.http import HttpResponse, JsonResponse
from slugify import slugify
from django.core import serializers
import json
import django

from .models import Leave, Application

class create_leave(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        try:
            data = request.data["body"]["data"]
            leave_form = Leave(leave_type=data["leave_type"],leave_slug=slugify(data["leave_type"]), leave_description=data["leave_description"], total_leaves_given=data["total_days"])
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
    permission_classes =(IsAuthenticated, )

    def post(self, request, pk):
        print(pk)
        print(request.data["body"])
        if request.data["body"]["data"] == "Approve":
            Application.objects.filter(pk=pk).update(approval="A")
        elif request.data["body"]["data"] == "Decline":
            Application.objects.filter(pk=pk).update(approval="R")
        return JsonResponse({"status": "success"})


class employee_records(APIView):
    def get(self, request):
        pass

class leave_application(APIView):
    def post(self, request, employee_id, leave_type):
        pass

class employee_leave_details(APIView):
    def get(self, request, employee_id):
        pass


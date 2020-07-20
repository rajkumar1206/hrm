from rest_framework.permissions import BasePermission
from employee.models import EmployeeType

class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        if EmployeeType.objects.filter(employee_id=request.user).exists():
            return True
        else:
            return False
        
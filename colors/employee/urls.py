from django.urls import path

from . import views

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('list/', views.employee_list.as_view(), name='employee_list'),
    path('list/employeeids/', views.employee_id_list.as_view(), name='employee_id_list'),
    path('create/', views.create_employee.as_view(), name='employee_create'),
    path('<str:employee_id>/delete/', views.delete_employee.as_view(), name='employee_delete'),
    path('<str:employee_id>/update/', views.update_employee.as_view(), name='employee_update'),
    path('<str:employee_id>/', views.employee_detail.as_view(), name='employee_details'),
]
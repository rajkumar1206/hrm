from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.employee_list, name='employee_list'),
    path('create/', views.create_employee, name='employee_create'),
    path('<str:employee_id>/delete/', views.delete_employee, name='employee_delete'),
    path('<str:employee_id>/update/', views.update_employee, name='employee_update'),
    path('<str:employee_id>/', views.employee_detail, name='employee_details'),
]
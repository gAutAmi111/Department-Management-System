# departments/urls.py
from django.urls import path
from . import views

app_name = 'departments'  # This registers the namespace

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('roles/dashboard/', views.role_dashboard, name='role_dashboard'),
    path('employees/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('employees/modify/<int:employee_id>/', views.modify_employee, name='modify_employee'),
    path('employees/delete/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('add/', views.add_department, name='add_department'),
    path('modify/<int:dept_id>/', views.modify_department, name='modify_department'),
    path('delete/<int:dept_id>/', views.delete_department, name='delete_department'),
    path('inactive/', views.inactive_departments, name='inactive_departments'),
    path('roles/add/', views.add_role, name='add_role'),
    path('roles/modify/<int:role_id>/', views.modify_role, name='modify_role'),
    path('roles/delete/<int:role_id>/', views.delete_role, name='delete_role'),
]
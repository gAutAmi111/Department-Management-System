from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_department, name='add_department'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('modify/<int:dept_id>/', views.modify_department, name='modify_department'),
    path('delete/<int:dept_id>/', views.delete_department, name='delete_department'),
    path('inactive/', views.inactive_departments, name='inactive_departments'),
path('test-logout-page/', views.test_logout_page, name='test_logout_page'),
path('roles/dashboard/', views.role_dashboard, name='role_dashboard'),
    path('roles/add/', views.add_role, name='add_role'),
    path('roles/modify/<int:role_id>/', views.modify_role, name='modify_role'),
    path('roles/delete/<int:role_id>/', views.delete_role, name='delete_role'),

]
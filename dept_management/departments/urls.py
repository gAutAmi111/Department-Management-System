from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_department, name='add_department'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('modify/<int:dept_id>/', views.modify_department, name='modify_department'),
    path('delete/<int:dept_id>/', views.delete_department, name='delete_department'),
    path('inactive/', views.inactive_departments, name='inactive_departments'),
path('test-logout-page/', views.test_logout_page, name='test_logout_page'),
]
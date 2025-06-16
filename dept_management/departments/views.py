from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Department

def is_admin(user):
    return user.is_authenticated and user.is_superuser

admin_required = user_passes_test(is_admin)

@login_required
@admin_required
def add_department(request):
    if request.method == 'POST':
        dept_name = request.POST.get('dept_name')
        description = request.POST.get('description')
        if dept_name and description:
            Department.objects.create(dept_name=dept_name, description=description)
            messages.success(request, 'Department created successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please fill in all fields.')
    return render(request, 'departments/add_department.html')

@login_required
@admin_required
def dashboard(request):
    search_query = request.GET.get('search', '')
    if search_query:
        departments = Department.objects.filter(dept_name__icontains=search_query, status=True)
    else:
        departments = Department.objects.filter(status=True)
    return render(request, 'departments/dashboard.html', {'departments': departments})

@login_required
@admin_required
def modify_department(request, dept_id):
    department = Department.objects.get(dept_id=dept_id, status=True)
    if request.method == 'POST':
        dept_name = request.POST.get('dept_name')
        description = request.POST.get('description')
        if dept_name and description:
            department.dept_name = dept_name
            department.description = description
            department.save()
            messages.success(request, 'Department updated successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please fill in all fields.')
    return render(request, 'departments/modify_department.html', {'department': department})

@login_required
@admin_required
def delete_department(request, dept_id):
    department = Department.objects.get(dept_id=dept_id, status=True)
    if request.method == 'POST':
        has_linked_employees = False  # Placeholder for employee check
        if has_linked_employees:
            messages.error(request, 'Please reassign employees to another department before deleting.')
            return redirect('dashboard')
        department.status = False
        department.save()
        messages.success(request, 'Department deleted successfully!')
        return redirect('dashboard')
    return render(request, 'departments/delete_department.html', {'department': department})

@login_required
@admin_required
def inactive_departments(request):
    departments = Department.objects.filter(status=False)
    return render(request, 'departments/inactive_departments.html', {'departments': departments})

def test_logout(request):
    return render(request, 'departments/test_logout.html')

from django.contrib.auth import logout as auth_logout

def custom_logout(request):
    auth_logout(request)
    return redirect('login')

def test_logout_page(request):
    return render(request, 'departments/test_logout_page.html')
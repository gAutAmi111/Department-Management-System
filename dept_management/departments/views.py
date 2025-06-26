from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout as auth_logout
from .models import Department, Role, Employee

# Custom test to check if user is an admin
def is_admin(user):
    return user.is_authenticated and user.is_superuser

admin_required = user_passes_test(is_admin)

# Department Management Views
@login_required
@admin_required
def add_department(request):
    if request.method == 'POST':
        dept_name = request.POST.get('dept_name')
        description = request.POST.get('description')
        if dept_name and description:
            Department.objects.create(dept_name=dept_name, description=description)
            messages.success(request, 'Department created successfully!')
            return redirect('departments:dashboard')
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
            return redirect('departments:dashboard')
        else:
            messages.error(request, 'Please fill in all fields.')
    return render(request, 'departments/modify_department.html', {'department': department})

@login_required
@admin_required
def delete_department(request, dept_id):
    department = Department.objects.get(dept_id=dept_id, status=True)
    if request.method == 'POST':
        # Placeholder for checking linked employees
        has_linked_employees = Employee.objects.filter(department_id=dept_id, is_active=True).exists()
        if has_linked_employees:
            messages.error(request, 'Please reassign employees to another department before deleting.')
            return redirect('departments:dashboard')
        department.status = False
        department.save()
        messages.success(request, 'Department deleted successfully!')
        return redirect('departments:dashboard')
    return render(request, 'departments/delete_department.html', {'department': department})

@login_required
@admin_required
def inactive_departments(request):
    departments = Department.objects.filter(status=False)
    return render(request, 'departments/inactive_departments.html', {'departments': departments})

# Role Management Views
@login_required
@admin_required
def role_dashboard(request):
    roles = Role.objects.filter(is_active=True)
    if request.method == "GET" and 'search' in request.GET:
        search_query = request.GET.get('search', '')
        roles = roles.filter(role_name__icontains=search_query)
    return render(request, 'departments/role_dashboard.html', {'roles': roles})

@login_required
@admin_required
def add_role(request):
    if request.method == "POST":
        role_name = request.POST.get('role_name')
        description = request.POST.get('description')
        if role_name and description:
            Role.objects.create(role_name=role_name, description=description)
            messages.success(request, "Role created successfully!")
            return redirect('departments:role_dashboard')
        messages.error(request, "Role name and description are required.")
    return render(request, 'departments/add_role.html')

@login_required
@admin_required
def modify_role(request, role_id):
    role = get_object_or_404(Role, pk=role_id)
    if request.method == "POST":
        role.role_name = request.POST.get('role_name')
        role.description = request.POST.get('description')
        role.save()
        messages.success(request, "Role updated successfully!")
        return redirect('departments:role_dashboard')
    return render(request, 'departments/modify_role.html', {'role': role})

@login_required
@admin_required
def delete_role(request, role_id):
    role = get_object_or_404(Role, pk=role_id)
    if request.method == "POST":
        role.is_active = False  # Soft delete
        role.save()
        messages.success(request, "Role deleted successfully!")
        return redirect('departments:role_dashboard')
    return render(request, 'departments/delete_role.html', {'role': role})

# Employee Management Views
@login_required
@admin_required
def employee_dashboard(request):
    search_query = request.GET.get('search', '')
    if search_query:
        employees = Employee.objects.filter(first_name__icontains=search_query, is_active=True)
    else:
        employees = Employee.objects.filter(is_active=True)
    return render(request, 'departments/employee_dashboard.html', {'employees': employees})

@login_required
@admin_required
def add_employee(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        mobile_number = request.POST['mobile_number']
        department_id = request.POST['department']
        role_id = request.POST['role']
        reporting_manager_id = request.POST.get('reporting_manager')
        date_of_joining = request.POST['date_of_joining']
        username = request.POST['username']
        password = request.POST['password']
        
        employee = Employee(
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile_number=mobile_number,
            department_id=department_id,
            role_id=role_id,
            reporting_manager_id=reporting_manager_id,
            date_of_joining=date_of_joining,
            username=username,
            password=password
        )
        employee.save()
        messages.success(request, 'Employee added successfully!')
        return redirect('departments:employee_dashboard')
    departments = Department.objects.filter(status=True)
    roles = Role.objects.filter(is_active=True)
    managers = Employee.objects.filter(role__role_name__in=['Manager', 'Team Leader'], is_active=True)
    context = {'departments': departments, 'roles': roles, 'managers': managers}
    return render(request, 'departments/add_employee.html', context)

@login_required
@admin_required
def modify_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        employee.first_name = request.POST['first_name']
        employee.last_name = request.POST['last_name']
        employee.email = request.POST['email']
        employee.mobile_number = request.POST['mobile_number']
        employee.department_id = request.POST['department']
        employee.role_id = request.POST['role']
        employee.reporting_manager_id = request.POST.get('reporting_manager')
        employee.date_of_joining = request.POST['date_of_joining']
        employee.username = request.POST['username']
        if request.POST['password']:
            employee.password = request.POST['password']
        employee.save()
        messages.success(request, 'Employee updated successfully!')
        return redirect('departments:employee_dashboard')
    departments = Department.objects.filter(status=True)
    roles = Role.objects.filter(is_active=True)
    managers = Employee.objects.exclude(pk=employee_id).filter(is_active=True)
    context = {'employee': employee, 'departments': departments, 'roles': roles, 'managers': managers}
    return render(request, 'departments/update_employee.html', context)

@login_required
@admin_required
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        employee.is_active = False  
        employee.save()
        messages.success(request, 'Employee deleted successfully!')
        return redirect('departments:employee_dashboard')
    return render(request, 'departments/delete_employee.html', {'employee': employee})

# Authentication Views
def custom_logout(request):
    auth_logout(request)
    return redirect('login')

def test_logout(request):
    return render(request, 'departments/test_logout.html')

def test_logout_page(request):
    return render(request, 'departments/test_logout_page.html')
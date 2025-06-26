from django.db import models

class Department(models.Model):
    dept_id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)  # True for active, False for inactive (soft delete)

    def __str__(self):
        return self.dept_name

class Role(models.Model):
    role_name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.role_name

    class Meta:
        db_table = 'roles'

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)  # Note: Use Django's authentication system for secure password handling in production
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='employees')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='employees')
    reporting_manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')
    date_of_joining = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)  # Soft delete flag

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'users'  # Matches the table name from the database design image
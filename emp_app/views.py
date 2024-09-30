from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Employee, Department, Role
from .forms import CreateUserForm

def superuser_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, "You need to be an admin to access add and delete employee pages.")
            return redirect('index')  
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Index view with login required
@login_required(login_url='login_page')
def index(request):
    return render(request, 'index.html')

# Adding employee
@superuser_required
def add_emp(request):
    if request.method == "POST":
        # Capture form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        salary = request.POST.get('salary')
        bonus = request.POST.get('bonus')
        phone_number = request.POST.get('phone_number')
        hire_date = request.POST.get('hire_date')
        dept_id = request.POST.get('dept')
        role_id = request.POST.get('role')

        # Save new employee instance
        employee = Employee(
            first_name=first_name,
            last_name=last_name,
            salary=salary,
            bonus=bonus,
            phone_number=phone_number,
            hire_date=hire_date,
            dept_id=dept_id,
            role_id=role_id,
        )
        employee.save()

        departments = Department.objects.all()
        roles = Role.objects.all()
        context = {
            'departments': departments,
            'roles': roles,
            'success_message': "New Employee has been added successfully!"
        }
        return render(request, 'add_emp.html', context)

    elif request.method == "GET":
        # Display the form for the first time
        departments = Department.objects.all()
        roles = Role.objects.all()
        context = {
            'departments': departments,
            'roles': roles
        }
        return render(request, 'add_emp.html', context)

# Removing employee
@superuser_required
def remove_emp(request):
    employee = None
    emp_list = Employee.objects.all()
    success_message = None
    employee_deleted = False

    if request.method == "POST":
        sno = request.POST.get('sno')

        try:
            employee = Employee.objects.get(sno=sno)
            if request.POST.get('confirm') == "true":
                employee.delete()
                success_message = "Employee has been removed successfully!"
                employee_deleted = True

        except Employee.DoesNotExist:
            return HttpResponse("""<h2 style="text-align: center;">Employee with the given Serial Number not found. Please try again.</h2>""")

    context = {
        'employee': employee if not employee_deleted else None,
        'emp_list': emp_list,
        'success_message': success_message,
    }

    return render(request, 'remove_emp.html', context)

# Filter employees
def filter_emp(request):
    emp_list = Employee.objects.all()
    context = {
        'emp_list': emp_list,
    }
    return render(request, 'filter_emp.html', context)

# View all employees
def view_all_emp(request):
    template = loader.get_template('view_all_emp.html')
    emp_list = Employee.objects.all()
    context = {
        'emp_list': emp_list,
    }
    return HttpResponse(template.render(context, request))

# Authentication views
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User Created Successfully")
            return redirect('login_page') 
        else:
            messages.error(request, "There was an error creating your account. Please correct the errors below.")
    else:
        form = CreateUserForm()

    context = {
        'form': form
    }

    return render(request, 'register.html', context)

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to the index page after login
        else:
            messages.error(request, "Invalid username or password.")

    context = {
        'messages': messages.get_messages(request)
    }
    return render(request, 'loginPage.html', context)

def log_out(request):
    logout(request)
    return redirect('login_page')

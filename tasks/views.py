from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Task, Employee
from .forms import TaskForm, SignUpForm, EmployeeForm


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Employee.objects.create(user=user, role='employee')
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'tasks/signup.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'tasks/login.html'


def is_manager_user(user):
    return (
        user.is_superuser or user.is_staff or
        Employee.objects.filter(user=user, role__in=['admin', 'manager']).exists()
    )


@login_required
def dashboard(request):
    is_manager = is_manager_user(request.user)

    if is_manager:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(assigned_to=request.user)

    status_filter = request.GET.get('status')
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    context = {
        'tasks': tasks,
        'is_manager': is_manager,
        'status_choices': Task.STATUS_CHOICES,
    }
    return render(request, 'tasks/dashboard.html', context)


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task created successfully.')
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Create Task'})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Update Task'})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted.')
        return redirect('dashboard')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


@login_required
def task_status_update(request, pk):
    task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Task.STATUS_CHOICES):
            task.status = new_status
            task.save()
    return redirect('dashboard')


# ---------------- Employee Management (admin-panel style) ----------------

@login_required
def employee_list(request):
    if not is_manager_user(request.user):
        messages.error(request, "You don't have permission to view this page.")
        return redirect('dashboard')
    employees = Employee.objects.select_related('user').all()
    return render(request, 'tasks/employee_list.html', {'employees': employees})


@login_required
def employee_create(request):
    if not is_manager_user(request.user):
        return redirect('dashboard')
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee added successfully.')
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'tasks/employee_form.html', {'form': form, 'title': 'Add Employee'})


@login_required
def employee_update(request, pk):
    if not is_manager_user(request.user):
        return redirect('dashboard')
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully.')
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'tasks/employee_form.html', {'form': form, 'title': 'Edit Employee'})


@login_required
def employee_delete(request, pk):
    if not is_manager_user(request.user):
        return redirect('dashboard')
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee removed.')
        return redirect('employee_list')
    return render(request, 'tasks/employee_confirm_delete.html', {'employee': employee})
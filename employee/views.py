import json
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.http import JsonResponse
from employee.forms import EmployeeForm
from employee.models import Employee

# Create your views here.

def get_next_eid():
    last_employee = Employee.objects.order_by('-id').first()
    if last_employee and last_employee.eid.isdigit():
        return str(int(last_employee.eid) + 1)
    return '1'

def emp(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        eid = request.POST.get('eid')
        
        if Employee.objects.filter(eid=eid).exists():
            messages.error(request, "Employee ID already exists. Please use a different ID.")
            return render(request, 'employee/index.html', {'form': form})
        
        if form.is_valid():
            form.save()
            return redirect('/show')
    else:
        next_eid = get_next_eid()
        form = EmployeeForm()
    
    return render(request, 'employee/index.html', {'form': form, 'next_eid': next_eid})

def main(request):
    return render(request,'employee/main.html')

def show(request):
    employees = Employee.objects.all()
    return render(request,"employee/show.html",{'employees':employees})

def edit(request, id):
    employee = Employee.objects.get(id=id)
    return render(request,'employee/edit.html', {'employee':employee})

def update(request, id):
    employee = Employee.objects.get(id=id)
    form = EmployeeForm(request.POST, instance = employee)
    if form.is_valid():
        form.save()
        return redirect("/show")
    return render(request, 'employee/edit.html', {'employee': employee})

def destroy(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee_name = employee.ename
    employee_id = employee.eid
    employee.delete()

    messages.success(request, f"Employee {employee_id}-{employee_name} has been deleted successfully.")

    return redirect("/show")

def check_employee_id(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        eid = data.get('eid')
        is_unique = not Employee.objects.filter(eid=eid).exists()

        return JsonResponse({'isUnique': is_unique})
    
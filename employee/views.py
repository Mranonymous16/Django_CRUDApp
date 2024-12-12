import json
from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render, redirect
from employee.forms import EmployeeForm
from employee.models import Employee
# Create your views here.
def emp(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/show')
            except:
                pass
    else:
        form = EmployeeForm()
    return render(request,'employee/index.html',{'form':form})
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
    employee = Employee.objects.get(id=id)
    employee.delete()
    return redirect("/show")

def check_employee_id(request):
    if request.method == 'POST':
        # Get the Employee ID from the request body
        data = json.loads(request.body)
        eid = data.get('eid')

        # Check if the Employee ID already exists
        is_unique = not Employee.objects.filter(eid=eid).exists()

        return JsonResponse({'isUnique': is_unique})
    
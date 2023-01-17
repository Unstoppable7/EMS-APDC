from django.shortcuts import render
from .forms import EmployeeForm, ApplicationForm, MedicalFormForm, DocumentForm,EmergencyContactForm
from django.shortcuts import redirect
from django.http import HttpResponse

# Create your views here.
def create_employee_application(request):
    if request.method == 'POST':
        employee_form  = EmployeeForm(request.POST)
        application_form  = ApplicationForm(request.POST)
        medicalForm_form  = MedicalFormForm(request.POST)
        emergency_contact_form  = EmergencyContactForm(request.POST)

        if employee_form.is_valid() and application_form.is_valid() and medicalForm_form.is_valid() and emergency_contact_form.is_valid():

            employee = employee_form.save()
            application = application_form.save(commit=False)
            application.employee = employee
            application.save()
            medical = medicalForm_form.save(commit=False)
            medical.employee = employee
            medical.save()
            emergency_contact = emergency_contact_form.save(commit=False)
            emergency_contact.employee = employee
            emergency_contact.save()
            # print("\n\n")
            # print(employee)
            # print("\n\n")
            # print(application)
            # print("\n\n")
            # print(medical)
            # print("\n\n")
            # print(emergency_contact)
            # print("\n\n")

            return HttpResponse("HttpResponse")
            #return redirect('employee_detail', pk=employee.pk)
            #     return HttpResponse("HttpResponse")
        else:
            print('NO VALID')
    else:
        employee_form = EmployeeForm()
        application_form = ApplicationForm()
        medicalForm_form = MedicalFormForm()
        emergency_contact_form = EmergencyContactForm()

    return render(request, 'employee_form.html', {'employee_form': employee_form, 'application_form': application_form, 'emergency_contact_form': emergency_contact_form, 'medicalForm_form': medicalForm_form,})

def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save()
            return redirect('application_detail', pk=application.pk)
    else:
        form = ApplicationForm()
    return render(request, 'application_form.html', {'form': form})

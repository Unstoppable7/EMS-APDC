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
        #document_form = DocumentForm(request.POST, request.FILES)

        # if employee_form.is_valid() and application_form.is_valid() and medicalForm_form.is_valid() and emergency_contact_form.is_valid() and document_form.is_valid():
        #     return HttpResponse("HttpResponse")

        if employee_form.is_valid() and application_form.is_valid() and medicalForm_form.is_valid() and emergency_contact_form.is_valid():
            #return HttpResponse("HttpResponse")
            employee_form.save()
            application_form.save()
            medicalForm_form.save()
            emergency_contact_form.save()
            #return redirect('employee_detail', pk=employee.pk)

        # if document_form.is_valid():
            
        #     #document_form.save()
        #     #return redirect('employee_detail', pk=employee.pk)

        #     return HttpResponse("HttpResponse")
        # else:
        #     print(document_form.errors.as_json())
    else:
        employee_form = EmployeeForm()
        application_form = ApplicationForm()
        medicalForm_form = MedicalFormForm()
        emergency_contact_form = EmergencyContactForm()
        #document_form = DocumentForm()

    return render(request, 'employee_form.html', {'employee_form': employee_form, 'application_form': application_form, 'emergency_contact_form': emergency_contact_form, 'medicalForm_form': medicalForm_form,})

    # return render(request, 'employee_form.html', {'document_form':document_form})

def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save()
            return redirect('application_detail', pk=application.pk)
    else:
        form = ApplicationForm()
    return render(request, 'application_form.html', {'form': form})

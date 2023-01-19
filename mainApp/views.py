from django.shortcuts import render
from .forms import EmployeeForm, ApplicationForm, MedicalFormForm, DocumentForm,EmergencyContactForm
from django.shortcuts import redirect
from django.http import HttpResponse

from django.http import FileResponse
from django.template.loader import render_to_string
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

from django.template.loader import get_template
from xhtml2pdf import pisa

def render_to_pdf(string):
    #template = get_template(template_src)
    #html  = template.render(context_dict)
    html = string
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode()), result)
    if not pdf.err:

        print(result.getvalue())

        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

# Create your views here.
def create_employee_application(request):
    if request.method == 'POST':
        employee_form  = EmployeeForm(request.POST)
        application_form  = ApplicationForm(request.POST)
        medicalForm_form  = MedicalFormForm(request.POST)
        emergency_contact_form  = EmergencyContactForm(request.POST)

        if employee_form.is_valid() and application_form.is_valid() and medicalForm_form.is_valid() and emergency_contact_form.is_valid():

            # employee = employee_form.save()
            # application = application_form.save(commit=False)
            # application.employee = employee
            # application.save()
            # medical = medicalForm_form.save(commit=False)
            # medical.employee = employee
            # medical.save()
            # emergency_contact = emergency_contact_form.save(commit=False)
            # emergency_contact.employee = employee
            # emergency_contact.save()

            # Create an instance of the model form with data from the model
            #form = MyModelForm(instance=MyModel.objects.get(pk=1))

            # string = render_to_string('employee_form.html', {'employee_form': employee_form, 'application_form': application_form, 'emergency_contact_form': emergency_contact_form, 'medicalForm_form': medicalForm_form,})

            # # Render the form as a string
            # form_html = render_to_pdf(string)

            # Create a file-like buffer to receive PDF data.
            # buffer = BytesIO()

            # # Create the PDF object, using the buffer as its "file."
            # p = canvas.Canvas(buffer, pagesize=letter)
            
            # styles = getSampleStyleSheet()
            # para = Paragraph("Texto con estilo", style=styles["Normal"])
            # # Dibujar el párrafo en el canvas
            # para.drawOn(p, 100, 700)
            # Draw the form on the PDF
            #p.drawString(100, 750, form_html)

            #p.drawString(100, 750, "<div id='div_id_name' class='form-group'>")
            # p.drawString(100, 740, "<label for='id_name' class='requiredField'>")
            # p.drawString(100, 730, "Write your name as it appears on your ID<span class='asteriskField'>*</span>")
            # p.drawString(100, 720, "</label>")
            # p.drawString(100, 710, "<div>")
            # p.drawString(100, 700, "<input type='text' name='name' value='Cristian Rosales' maxlength='100'")
            # p.drawString(100, 690, "class='textinput textInput form-control' required id='id_name'>")
            # p.drawString(100, 680, "</div>")
            # p.drawString(100, 670, "</div>")

            # Close the PDF object cleanly, and we're done.
            # p.showPage()
            # p.save()

            #buffer.seek(0)
            #return FileResponse(, as_attachment=True, filename='myform.pdf')


            # print("\n\n")
            # print(employee)
            # print("\n\n")
            # print(application)
            # print("\n\n")
            # print(medical)
            # print("\n\n")
            # print(emergency_contact)
            # print("\n\n")


            #return HttpResponse(form_html, content_type='application/pdf')

            #return redirect('employee_detail', pk=employee.pk)
            return HttpResponse("HttpResponse")
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

from django.shortcuts import render
from .forms import EmployeeForm, AddressForm, ApplicationForm, MedicalFormForm,EmergencyContactForm
from .models import Document
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import FileResponse
from django.template.loader import render_to_string
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, TableStyle
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from django.core.files.base import ContentFile
from django.conf import settings

from django.conf import settings    

def form_to_pdf(employeeForm, addressForm, applicationForm, medicalForm, emergency_contactForm):

    name_label_text = "Names"
    last_name_label_text = "Surnames"
    street_street_address_label_text = "Street Address"
    unit_number_label_text = "Apartment, unit, suite, or floor #"
    city_label_text = "City"
    state_label_text = "State"
    zipcode_label_text = "Zip code"
    email_label_text = "Email"
    phone_label_text = "Phone number"
    date_birth_label_text = "Date of birth"


    days_available_label_text = "Days available to work"
    can_travel_label_text = "If the job requires it, can you travel?"
    desired_job_label_text = "Desired job"
    can_work_nights_label_text = "Can you work nights?"
    position_to_apply_label_text = "Position to which applies"
    desired_payment_label_text = "Desired payment"
    worked_for_this_company_before_label_text = "Have you worked for this company before?. If the answer is yes, indicate the start date and end date"
    has_been_convicted_of_a_felony_label_text = "Have you ever been convicted of a felony?. If the answer is yes, explain "
    can_background_check_label_text = "Are you open to a background check?"
    test_controlled_substances_label_text = "If hired, are you willing to test for controlled substances? "


    experience_label_text = "Mention the jobs in which you have experience"
    english_level_label_text = "English language level"
    studies_label_text = "Indicate the studies you have carried out "
    specialty_of_studies_label_text = "Specialty of your studies"


    military_service_label_text = "Have you ever been a member of the united states armed services? "
    service_branch_label_text = "Service branch"
    start_period_service_label_text = "Start period"
    end_period_service_label_text = "End period"
    duties_training_service_label_text = "Describe your duties and any special training"

    
    emergency_contact_name_label_text = "Name"
    emergency_contact_phone_number_label_text = "Phone number"
    relationship_label_text = "Relationship"


    full_name_label_text = "Full Name"
    height_label_text = "Height"
    weight_label_text = "Weight"
    allergic_to_label_text = "Mention any allergies you have"
    diseases_suffered_label_text = "Mention the diseases you suffer from"
    received_workers_compensation_label_text = "Have you ever received workers compensation due to an injury at work? If the answer is yes, describe why?"
    received_surgery_for_fracture_label_text = "Have you received surgery for a fracture? If the answer is yes, describe all the details"
    physical_disability_evaluation_label_text = "Have you received any kind of physical disability evaluation or assigned by any insurance company or state/or federal agency? If the answer is yes, describe why, when and where"

    employee = employeeForm.save(commit=False)

    buffer = BytesIO()

    # Create a PDF document
    #pdf_file = SimpleDocTemplate("form.pdf", pagesize=letter)
    pdf_file = SimpleDocTemplate(buffer, pagesize=letter)
    
    styles = getSampleStyleSheet()

    form_title = styles['Title']
    form_title.spaceAfter = 10
    title_style = ParagraphStyle(name='TitleStyle',
                            fontName='Helvetica-Bold',
                            fontSize=18,
                            alignment = 1,
                             )

    section_style = ParagraphStyle(name='SectionStyle',
                             fontName = 'Helvetica-bold',
                             fontSize = 12,
                             leading = 18,
                             alignment = 1,
                             borderColor = colors.black,
                             borderWidth = 1,
                             borderPadding = 1,
                             backColor = colors.lightblue,
                             textColor = colors.black,
                             bulletIndent = 0
                             )

    label_style = ParagraphStyle(name='LabelStyle',
                             fontName='Helvetica-Bold',
                             fontSize=12,
                             textColor=colors.black,
                             )
    field_style = ParagraphStyle(name='FieldStyle',
                             fontName='Helvetica',
                             fontSize=12,
                             textColor=colors.black,
                             )

    elements = []

    #-----Paragraphs-----
    applicationTitle = Paragraph("APPLICATION", title_style)
    
    personal_information = Paragraph("PERSONAL INFORMATION", section_style)
    name_label = Paragraph(name_label_text, label_style)
    name_field = Paragraph(employeeForm.cleaned_data['first_name'], field_style)
    last_name_label = Paragraph(last_name_label_text, label_style)
    last_name_field = Paragraph(employeeForm.cleaned_data['last_name'], field_style)
    data1rows1 = [[name_label,name_field,last_name_label,last_name_field]]
    table1rows1 = Table(data1rows1, colWidths=[90,150,90,None])
    table1rows1.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

    street_address_label = Paragraph(street_street_address_label_text, label_style)
    street_address_field = Paragraph(addressForm.cleaned_data['street'], field_style)
    unit_number_label = Paragraph(unit_number_label, label_style)
    unit_number_field = Paragraph(addressForm.cleaned_data['unit_number'], field_style)
    data2rows1 = [[street_address_label,street_address_field, unit_number_label,unit_number_field]]
    table2rows1 = Table(data2rows1, colWidths=[75,180,75,None])
    table2rows1.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

    city_label = Paragraph(city_label_text, label_style)
    city_field = Paragraph(str(addressForm.cleaned_data['city_name']).capitalize(), field_style)

    state_label = Paragraph(state_label_text, label_style)
    state_field = Paragraph(str(addressForm.cleaned_data['state_name']), field_style)

    zipcode_label = Paragraph(zipcode_label_text, label_style)
    zipcode_field = Paragraph(addressForm.cleaned_data['zip_code'], field_style)
    data3rows1 = [[city_label, city_field, state_label,state_field,zipcode_label,zipcode_field]]
    table3rows1 = Table(data3rows1, colWidths=[45,None,55,None,80,None])
    table3rows1.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

    # email_label = Paragraph(employeeForm['email'].label, label_style)
    email_label = Paragraph(email_label_text, label_style)
    email_field = Paragraph(employeeForm.cleaned_data['email'], field_style)
    # phone_label = Paragraph(employeeForm['phone_number'].label, label_style)
    phone_label = Paragraph(phone_label_text, label_style)
    phone_field = Paragraph(employeeForm.cleaned_data['phone_number'], field_style)
    data4rows1 = [[email_label, email_field, phone_label,phone_field]]
    table4rows1 = Table(data4rows1, colWidths=[55,None,120,None])
    table4rows1.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

    # date_birth_label = Paragraph(employeeForm['date_of_birth'].label, label_style)
    date_birth_label = Paragraph(date_birth_label_text, label_style)
    date_birth_field = Paragraph(employeeForm.cleaned_data['date_of_birth'].strftime("%m/%d/%Y"), field_style)
    data5rows1 = [[date_birth_label, date_birth_field]]
    table5rows1 = Table(data5rows1, colWidths=[100,None])
    table5rows1.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1),'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

    section_employment_eligibility = Paragraph("EMPLOYMENT ELIGIBILITY", section_style)

    # days_available_label = Paragraph(applicationForm['days_available_to_work'].label, label_style)
    days_available_label = Paragraph(days_available_label_text, label_style)
    days_available_field = Paragraph(applicationForm.cleaned_data['days_available_to_work'], field_style)
    data6rows1 = [[days_available_label, days_available_field]]
    table6rows1 = Table(data6rows1, colWidths=[175,None])
    table6rows1.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1),'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))  

    # can_travel_label = Paragraph(applicationForm.['can_travel'].label, label_style)
    can_travel_label = Paragraph(can_travel_label_text, label_style)
    if applicationForm.cleaned_data['can_travel'] is True:
        can_travel_field = Paragraph('Yes', field_style)
    else:
        can_travel_field = Paragraph('No', field_style)
    data7rows1 = [[can_travel_label, can_travel_field]]
    table7rows1 = Table(data7rows1, colWidths=[260,None])
    table7rows1.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1),'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

    # desired_job_label = Paragraph(applicationForm['desired_job'].label, label_style)
    desired_job_label = Paragraph(desired_job_label_text, label_style)
    desired_job_field = Paragraph(applicationForm.cleaned_data['desired_job'], field_style)
    # can_work_nights_label = Paragraph(applicationForm['can_work_nights'].label, label_style)
    can_work_nights_label = Paragraph(can_work_nights_label_text, label_style)
    if applicationForm.cleaned_data['can_work_nights'] is True:
        can_work_nights_field = Paragraph('Yes', field_style)
    else:
        can_work_nights_field = Paragraph('No', field_style)
    data8rows1 = [[desired_job_label, desired_job_field, can_work_nights_label, can_work_nights_field]]
    table8rows1 = Table(data8rows1, colWidths=[100,None,165,None])
    table8rows1.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1),'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

    # position_to_apply_label = Paragraph(applicationForm['position_to_apply'].label, label_style)
    position_to_apply_label = Paragraph(position_to_apply_label_text, label_style)
    position_to_apply_field = Paragraph(applicationForm.cleaned_data['position_to_apply'], field_style)  
    # desired_payment_label = Paragraph(applicationForm['desired_payment'].label, label_style)
    desired_payment_label = Paragraph(desired_payment_label_text, label_style)
    desired_payment_field = Paragraph(applicationForm.cleaned_data['desired_payment'], field_style)
    data9rows1 = [[position_to_apply_label, position_to_apply_field,desired_payment_label,desired_payment_field]]
    table9rows1 = Table(data9rows1, colWidths=[135,None,135,None])
    table9rows1.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1),'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
])) 

    # worked_for_this_company_before_label = Paragraph(applicationForm['worked_for_this_company_before'].label, label_style)
    worked_for_this_company_before_label = Paragraph(worked_for_this_company_before_label_text, label_style)
    worked_for_this_company_before_field = Paragraph(applicationForm.cleaned_data['worked_for_this_company_before'], field_style)  
    data10rows1 = [[worked_for_this_company_before_label, worked_for_this_company_before_field]]
    table10rows1 = Table(data10rows1, colWidths=[None])
    table10rows1.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1),'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

    # has_been_convicted_of_a_felony_label = Paragraph(applicationForm['has_been_convicted_of_a_felony'].label, label_style)
    has_been_convicted_of_a_felony_label = Paragraph(has_been_convicted_of_a_felony_label_text, label_style)
    has_been_convicted_of_a_felony_field = Paragraph(applicationForm.cleaned_data['has_been_convicted_of_a_felony'], field_style)  
    data11rows1 = [[has_been_convicted_of_a_felony_label, has_been_convicted_of_a_felony_field]]
    table11rows1 = Table(data11rows1, colWidths=[None])
    table11rows1.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1),'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))
        
    # can_background_check_label = Paragraph(applicationForm['can_background_check'].label, label_style)
    can_background_check_label = Paragraph(can_background_check_label_text, label_style)
    if applicationForm.cleaned_data['can_background_check'] is True:
        can_background_check_field = Paragraph('Yes', field_style)
    else:
        can_background_check_field = Paragraph('No', field_style)
      
    data12rows1 = [[can_background_check_label, can_background_check_field]]
    table12rows1 = Table(data12rows1, colWidths=[None])
    table12rows1.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1),'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

    # test_controlled_substances_label = Paragraph(applicationForm['test_controlled_substances'].label, label_style)
    test_controlled_substances_label = Paragraph(test_controlled_substances_label_text, label_style)
    #test_controlled_substances_field = Paragraph(applicationForm.cleaned_data['test_controlled_substances'], field_style)

    if applicationForm.cleaned_data['test_controlled_substances'] is True:
        test_controlled_substances_field = Paragraph('Yes', field_style)
    else:
        test_controlled_substances_field = Paragraph('No', field_style)

    data13rows1 = [[test_controlled_substances_label, test_controlled_substances_field]]
    table13rows1 = Table(data13rows1, colWidths=[None])
    table13rows1.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1),'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

    section_experience = Paragraph("EXPERIENCE/SKILLS", section_style)

    # experience_label = Paragraph(applicationForm['experience_jobs'].label, label_style)
    experience_label = Paragraph(experience_label_text, label_style)
    experience_field = Paragraph(','.join(applicationForm.cleaned_data['experience_jobs']), field_style)
    data14rows1 = [[experience_label, experience_field]]
    table14rows1 = Table(data14rows1, colWidths=[None])
    table14rows1.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1),'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

    # english_level_label = Paragraph(applicationForm['english_level'].label, label_style)
    english_level_label = Paragraph(english_level_label_text, label_style)
    english_level_field = Paragraph(applicationForm.cleaned_data['english_level'], field_style)
    data15rows1 = [[english_level_label, english_level_field]]
    table15rows1 = Table(data15rows1, colWidths=[150,None])
    table15rows1.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1),'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

    section_education = Paragraph("EDUCATION", section_style)

    # studies_label = Paragraph(applicationForm['studies'].label, label_style)
    studies_label = Paragraph(studies_label_text, label_style)
    studies_field = Paragraph(applicationForm.cleaned_data['studies'], field_style)
    data16rows1 = [[studies_label, studies_field]]
    table16rows1 = Table(data16rows1, colWidths=[250,None])
    table16rows1.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1),'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

    # specialty_of_studies_label = Paragraph(applicationForm['specialty_of_studies'].label, label_style)
    specialty_of_studies_label = Paragraph(specialty_of_studies_label_text, label_style)
    specialty_of_studies_field = Paragraph(applicationForm.cleaned_data['specialty_of_studies'], field_style)
    data17rows1 = [[specialty_of_studies_label, specialty_of_studies_field]]
    table17rows1 = Table(data17rows1, colWidths=[250,None])
    table17rows1.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1),'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

    section_military_service = Paragraph("MILITARY SERVICE", section_style)

    # military_service_label = Paragraph(applicationForm['military_service'].label, label_style)
    military_service_label = Paragraph(military_service_label_text, label_style)
    if applicationForm.cleaned_data['military_service'] is True:
        military_service_field = Paragraph('Yes', field_style)
    else:
        military_service_field = Paragraph('No', field_style)

    data18rows1 = [[military_service_label, military_service_field]]
    table18rows1 = Table(data18rows1, colWidths=[250,None])
    table18rows1.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1),'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

    # service_branch_label = Paragraph('Service Branch', label_style)
    service_branch_label = Paragraph(service_branch_label_text, label_style)
    service_branch_field = Paragraph(applicationForm.cleaned_data['service_branch'], field_style)
    data19rows1 = [[service_branch_label, service_branch_field]]
    table19rows1 = Table(data19rows1, colWidths=[100,None])
    table19rows1.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1),'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

    # start_period_service_label = Paragraph('Start Period', label_style)
    start_period_service_label = Paragraph(start_period_service_label_text, label_style)
    end_period_service_label = Paragraph(end_period_service_label_text, label_style)
    try:
        start_period_service_field = Paragraph(applicationForm.cleaned_data['start_period_service'].strftime("%m/%d/%Y"), field_style)
        end_period_service_field = Paragraph(applicationForm.cleaned_data['end_period_service'].strftime("%m/%d/%Y"), field_style)
    except:
        start_period_service_field = Paragraph("", field_style)
        end_period_service_field = Paragraph("", field_style)
    
    data20rows1 = [[start_period_service_label, start_period_service_field,end_period_service_label,end_period_service_field]]
    table20rows1 = Table(data20rows1, colWidths=[80,None,80,None])
    table20rows1.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1),'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

    # duties_training_service_label = Paragraph(applicationForm['duties_training_service'].label, label_style)
    duties_training_service_label = Paragraph(duties_training_service_label_text, label_style)
    duties_training_service_field = Paragraph(applicationForm.cleaned_data['duties_training_service'], field_style)
    data21rows1 = [[duties_training_service_label, duties_training_service_field]]
    table21rows1 = Table(data21rows1, colWidths=[None])
    table21rows1.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1),'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

    section_emergency_contact = Paragraph("EMERGENCY CONTACT", section_style)

    # emergency_contact_name_label = Paragraph(emergency_contactForm['name'].label, label_style)
    emergency_contact_name_label = Paragraph(emergency_contact_name_label_text, label_style)
    emergency_contact_name_field = Paragraph(emergency_contactForm.cleaned_data['name'], field_style)
    # emergency_contact_phone_number_label = Paragraph(emergency_contactForm['phone_number'].label, label_style)
    emergency_contact_phone_number_label = Paragraph(emergency_contact_phone_number_label_text, label_style)
    emergency_contact_phone_number_field = Paragraph(emergency_contactForm.cleaned_data['phone_number'], field_style)
    data22rows1 = [[emergency_contact_name_label, emergency_contact_name_field,emergency_contact_phone_number_label,emergency_contact_phone_number_field]]
    table22rows1 = Table(data22rows1, colWidths=[50,None,100,None])
    table22rows1.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1),'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))
    
    # relationship_label = Paragraph(emergency_contactForm['relationship'].label, label_style)
    relationship_label = Paragraph(relationship_label_text, label_style)
    relationship_field = Paragraph(emergency_contactForm.cleaned_data['relationship'], field_style)
    data23rows1 = [[relationship_label, relationship_field]]
    table23rows1 = Table(data23rows1, colWidths=[85,None])
    table23rows1.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1),'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

    medicalTitle = Paragraph("MEDICAL FORM", title_style)

    # full_name_label = Paragraph('Full Name:', label_style)
    full_name_label = Paragraph(full_name_label_text, label_style)
    full_name_field = Paragraph(employee.full_name, field_style)
    data24rows1 = [[full_name_label, full_name_field]]
    table24rows1 = Table(data24rows1, colWidths=[None])
    table24rows1.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1),'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

    # height_label = Paragraph(medicalForm['height'].label, label_style)
    height_label = Paragraph(height_label_text, label_style)
    height_field = Paragraph(str(medicalForm.cleaned_data['height']), field_style)
    # weight_label = Paragraph(medicalForm['weight'].label, label_style)
    weight_label = Paragraph(weight_label_text, label_style)
    weight_field = Paragraph(str(medicalForm.cleaned_data['weight']), field_style)
    data25rows1 = [[height_label, height_field,weight_label,weight_field]]
    table25rows1 = Table(data25rows1, colWidths=[150,None,185,None])
    table25rows1.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1),'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

    # allergic_to_label = Paragraph(medicalForm['allergic_to'].label, label_style)
    allergic_to_label = Paragraph(allergic_to_label_text, label_style)
    allergic_to_field = Paragraph(medicalForm.cleaned_data['allergic_to'], field_style)
    data26rows1 = [[allergic_to_label, allergic_to_field]]
    table26rows1 = Table(data26rows1, colWidths=[None])
    table26rows1.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1),'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

    # diseases_suffered_label = Paragraph(medicalForm['diseases_suffered'].label, label_style)
    diseases_suffered_label = Paragraph(diseases_suffered_label_text, label_style)
    diseases_suffered_field = Paragraph(','.join(medicalForm.cleaned_data['diseases_suffered']), field_style)

    data27rows1 = [[diseases_suffered_label, diseases_suffered_field]]
    table27rows1 = Table(data27rows1, colWidths=[None])
    table27rows1.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1),'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

    # received_workers_compensation_label = Paragraph(medicalForm['received_workers_compensation'].label, label_style)
    received_workers_compensation_label = Paragraph(received_workers_compensation_label_text, label_style)
    received_workers_compensation_field = Paragraph(medicalForm.cleaned_data['received_workers_compensation'], field_style)
    data28rows1 = [[received_workers_compensation_label, received_workers_compensation_field]]
    table28rows1 = Table(data28rows1, colWidths=[None])
    table28rows1.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1),'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

    # received_surgery_for_fracture_label = Paragraph(medicalForm['received_surgery_for_fracture'].label, label_style)
    received_surgery_for_fracture_label = Paragraph(received_surgery_for_fracture_label_text, label_style)
    received_surgery_for_fracture_field = Paragraph(medicalForm.cleaned_data['received_surgery_for_fracture'], field_style)
    data29rows1 = [[received_surgery_for_fracture_label, received_surgery_for_fracture_field]]
    table29rows1 = Table(data29rows1, colWidths=[None])
    table29rows1.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1),'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

    # physical_disability_evaluation_label = Paragraph(medicalForm['physical_disability_evaluation'].label, label_style)
    physical_disability_evaluation_label = Paragraph(physical_disability_evaluation_label_text, label_style)
    physical_disability_evaluation_field = Paragraph(medicalForm.cleaned_data['physical_disability_evaluation'], field_style)
    data30rows1 = [[physical_disability_evaluation_label, physical_disability_evaluation_field]]
    table30rows1 = Table(data30rows1, colWidths=[None])
    table30rows1.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1),'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))
    #-----append elements-----
    elements.append(applicationTitle)
    elements.append(Spacer(1, 20))
    elements.append(personal_information)
    elements.append(Spacer(1, 10))
    elements.append(table1rows1)
    elements.append(Spacer(1, 5))
    elements.append(table2rows1)
    elements.append(Spacer(1, 5))
    elements.append(table3rows1)
    elements.append(Spacer(1, 5))
    elements.append(table4rows1)
    elements.append(Spacer(1, 5))
    elements.append(table5rows1)
    elements.append(Spacer(1, 10))
    elements.append(section_employment_eligibility)
    elements.append(Spacer(1, 10))
    elements.append(table6rows1)
    elements.append(Spacer(1, 5))
    elements.append(table7rows1)
    elements.append(Spacer(1, 5))
    elements.append(table8rows1)
    elements.append(Spacer(1, 5))
    elements.append(table9rows1)
    elements.append(Spacer(1, 5))
    elements.append(table10rows1)
    elements.append(Spacer(1, 5))
    elements.append(table11rows1)
    elements.append(Spacer(1, 5))
    elements.append(table12rows1)
    elements.append(Spacer(1, 5))
    elements.append(table13rows1)
    elements.append(Spacer(1, 10))
    elements.append(section_experience)
    elements.append(Spacer(1, 10))
    elements.append(table14rows1)
    elements.append(Spacer(1, 5))
    elements.append(table15rows1)
    elements.append(Spacer(1, 10))
    elements.append(section_education)
    elements.append(Spacer(1, 10))
    elements.append(table16rows1)
    elements.append(Spacer(1, 5))
    elements.append(table17rows1)
    elements.append(Spacer(1, 10))
    elements.append(section_military_service)
    elements.append(Spacer(1, 10))
    elements.append(table18rows1)
    elements.append(Spacer(1, 5))
    elements.append(table19rows1)
    elements.append(Spacer(1, 5))
    elements.append(table20rows1)
    elements.append(Spacer(1, 5))
    elements.append(table21rows1)
    elements.append(Spacer(1, 10))
    elements.append(section_emergency_contact)
    elements.append(Spacer(1, 10))
    elements.append(table22rows1)
    elements.append(Spacer(1, 5))
    elements.append(table23rows1)
    elements.append(Spacer(1, 20))
    elements.append(medicalTitle)
    elements.append(Spacer(1, 20))
    elements.append(table24rows1)
    elements.append(Spacer(1, 5))
    elements.append(table25rows1)
    elements.append(Spacer(1, 5))
    elements.append(table26rows1)
    elements.append(Spacer(1, 5))
    elements.append(table27rows1)
    elements.append(Spacer(1, 5))
    elements.append(table28rows1)
    elements.append(Spacer(1, 5))
    elements.append(table29rows1)
    elements.append(Spacer(1, 5))
    elements.append(table30rows1)

    pdf_file.title = employee.full_name 
    pdf_file.build(elements) 

    buffer.seek(0)
    pdf = buffer.getvalue()
    pdf_content = ContentFile(pdf)
    pdf_content.name = employee.full_name + '.pdf'

    return pdf_content

# Create your views here.
def create_employee_application(request):
    if request.method == 'POST':
        employee_form = EmployeeForm(request.POST, prefix='employee')
        address_form = AddressForm(request.POST)
        application_form = ApplicationForm(request.POST)
        medicalForm_form = MedicalFormForm(request.POST)
        emergency_contact_form = EmergencyContactForm(request.POST)

        if employee_form.is_valid() and address_form.is_valid() and application_form.is_valid() and medicalForm_form.is_valid() and emergency_contact_form.is_valid():
            
            pdfFile = form_to_pdf(employee_form, address_form,application_form,medicalForm_form, emergency_contact_form)            
            
            employee = employee_form.save(commit=False)
            employee.save()

            address = address_form.save(commit=False)
            address.employee = employee
            address.save()

            application = application_form.save(commit=False)
            application.employee = employee
            application.save()

            medical = medicalForm_form.save(commit=False)
            medical.employee = employee
            medical.save()

            emergency_contact = emergency_contact_form.save(commit=False)
            emergency_contact.employee = employee
            emergency_contact.save()
            #handle_uploaded_file(pdfFile)
            documentObj = Document(type='Form', file=pdfFile, employee=employee)

            documentObj.save()

            # response = FileResponse(pdfFile, content_type='application/pdf')
            # response['Content-Disposition'] = 'inline; filename=form.pdf'
            
            # return response

            #return redirect('employee_detail', pk=employee.pk)
            return HttpResponse("Application completed successfully")
        else:
            print('NO VALID')
    else:
        employee_form = EmployeeForm(prefix='employee')
        address_form = AddressForm()
        application_form = ApplicationForm()
        medicalForm_form = MedicalFormForm()
        emergency_contact_form = EmergencyContactForm()

    return render(request, 'employee_form.html', {'employee_form': employee_form, 'address_form': address_form, 'application_form': application_form, 'emergency_contact_form': emergency_contact_form, 'medicalForm_form': medicalForm_form,'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY})

def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save()
            return redirect('application_detail', pk=application.pk)
    else:
        form = ApplicationForm()
    return render(request, 'application_form.html', {'form': form})

def autocomplete(request):       
    return render(request, 'googleMap.html', {'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY})
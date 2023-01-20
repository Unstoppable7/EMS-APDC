from django import forms
from .models import Employee,Application,Emergency_contact,Document,MedicalForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

class EmployeeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    class Meta:
        model = Employee
        fields = ['name','last_name','phone_number','date_of_birth','mail','address','city','zip_code',]
        labels = {
            'name':'Name',
            'last_name':'Last name',
            'mail':'email'
        }

class ApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
    
    DESIRED_JOB_CHOICES = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Seasonal', 'Seasonal'),
    ]

    class Meta:
        model = Application
        fields = ['days_available_to_work','can_travel','can_work_nights','can_background_check','position_to_apply','experience','english_level','studies','specialty_of_studies','military_service']
        labels = {
            'can_travel':'If the job requires it, can you travel?','can_work_nights':'Can you work nights?',
            'can_background_check':'Are you open to a background check?',
            'position_to_apply':'Position to which applies',
            'experience':'Write the jobs in which you have experience',
            'english_level':'English language level',
            'studies':'Indicate the studies you have carried out',
            'specialty_of_studies':'Specialty of your studies',
            'military_service':'Have you ever been a member of the united states armed services?'
            }
    ##Manejar en el HTML
    service_branch = forms.CharField(required=False)
    start_period_service = forms.DateField(required=False,label='Start Period')
    end_period_service = forms.DateField(required=False,label='End Period')
    duties_training_service = forms.CharField(label='Describe your duties and any special training',required=False)

    worked_for_this_company_before = forms.CharField(label='Have you worked for this company before?. If the answer is yes, indicate the start date and end date')
    has_been_convicted_of_a_felony = forms.CharField(label='Have you ever been convicted of a felony?. If the answer is yes, explain')
    test_controlled_substances = forms.CharField(label='If Hired, Are You Willing To Test For Controlled Substances?')
    desired_job = forms.ChoiceField(choices=DESIRED_JOB_CHOICES)
    desired_payment = forms.CharField()

class MedicalFormForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
#TODO
    class Meta:
        model = MedicalForm
        fields = ['height', 'weight', 'allergic_to', 'diseases_suffered', 'received_workers_compensation', 'received_surgery_for_fracture']
        labels = {
            'height':'Enter your height in feet',
            'weight':'Enter your weight in pounds',
            'allergic_to':'Mention any allergies you have',
            'diseases_suffered':'Mention all the diseases you suffer from',
            'received_workers_compensation':'Have you ever received workers compensation due to an injury at work? If the answer is yes, describe why?',
            'received_surgery_for_fracture':'Have you received surgery for a fracture? If the answer is yes, describe all the details'
        }
    
    physical_disability_evaluation = forms.CharField(label='Have you received any kind of physical disability evaluation or assigned by any insurance company or state/or federal agency? If the answer is yes, describe why, when and where')

class EmergencyContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.add_input(Submit('submit', 'Save'))

    class Meta:
        model = Emergency_contact
        fields = ['name', 'phone_number', 'relationship']
        labels = {'name': 'name'}

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['type','date_of_expiration', 'file']  
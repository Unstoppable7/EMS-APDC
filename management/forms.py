from django import forms
from .models import Employee,Application,Emergency_contact,MedicalForm,City,Address,State
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils.translation import gettext_lazy as _
from .utils import only_letters

class EmployeeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    class Meta:
        model = Employee
        fields = ['first_name','last_name','phone_number','date_of_birth','email']
        fields = ['first_name','last_name','phone_number','date_of_birth','email']
        labels = {
            'first_name': _('Names'),
            'last_name': _('Surnames'),
            'phone_number': _('Phone number'),
            'date_of_birth': _('Date of birth MONTH/DAY/YEAR'),
            'email': _('Email'),
        }
        error_messages = {
            NON_FIELD_ERRORS: {
            
                #'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
                'unique_together': _("There is already a person registered with %(field_labels)s"),
            }
        }
    
    def clean(self):
        cleaned_data = super().clean()
        for field in cleaned_data:
            
            try:
                #Eliminamos espacios en blanco
                cleaned_data[field] = cleaned_data[field].strip()
            except:
                pass

            if isinstance(cleaned_data[field], str):

                if field != "email":
                    cleaned_data[field] = cleaned_data[field].title()
                if field == "first_name" or field == "last_name":
                    only_letters(cleaned_data[field], self.fields[field].label)

        return cleaned_data
    
    def save(self, commit=True):
        employee = super().save(commit=False)
        #employee.city = self.cleaned_data['city_name']
        if commit:
            employee.save()
        return employee

class AddressForm(forms.ModelForm):
    city_name = forms.CharField(required=True, label=_('City'))
    state_name = forms.CharField(required=True, label=_('State'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.attrs['autocomplete'] = 'off'
        self.fields['street'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['unit_number'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['city_name'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['state_name'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['postal_code'].widget.attrs.update({'autocomplete': 'off'})

    class Meta:
        model = Address
        fields = ['street','unit_number','city_name','state_name','postal_code']
        labels = {
            'street': _('Street Address'),
            'unit_number': _('Apartment, unit, suite, or floor #'),
            'postal_code': _('Zip code'),
        }
    
    def clean_city_name(self):
        city_name = self.cleaned_data.get('city_name')
        city_name_formatted = city_name.title()
        
        city = City.objects.filter(name=city_name_formatted).first()
        if(city is None):
            
            raise forms.ValidationError(_("Please enter a valid city."))
        return city
    
    def clean_state_name(self):
        state_name = self.cleaned_data.get('state_name')
        state_name_formatted = state_name.title()
        
        state_code = State.objects.filter(state_code=state_name_formatted).first()
        state_name = State.objects.filter(name=state_name_formatted).first()
        if(state_code is None and state_name is None):
            
            raise forms.ValidationError(_("Please enter a valid state."))
        
        if(state_code is not None):

            return state_code
        else:
            return state_name

    def clean(self):
        cleaned_data = super().clean()
        for field in cleaned_data:
            
            try:
                #Eliminamos espacios en blanco
                cleaned_data[field] = cleaned_data[field].strip()
            except:
                pass

            if isinstance(cleaned_data[field], str):

                cleaned_data[field] = cleaned_data[field].title()
                if field == "city_name" or field == "state_name":
                    cleaned_data[field] = cleaned_data[field].title()
                if field == "city_name" or field == "state_name":
                    only_letters(cleaned_data[field], self.fields[field].label)

        return cleaned_data
    
    def save(self, commit=True):
        address = super().save(commit=False)
        
        address.city = self.cleaned_data['city_name']
        address.state = self.cleaned_data['state_name']

        address = super().save(commit=False)
        
        address.city = self.cleaned_data['city_name']
        address.state = self.cleaned_data['state_name']

        if commit:
            address.save()
        return address

class ApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    experience_jobs = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=[('Manager', 'Manager'),
        ('Housekeeping', 'Housekeeping'),
        ('Houseman', 'Houseman'),
        ('Community Areas', 'Community Areas'),
        ('Housekeeping Supervisor', 'Housekeeping Supervisor'),
        ('Housekeeping Inspector', 'Housekeeping Inspector'),
        ('Cook', 'Cook'),
        ('Precook', 'Precook'),
        ('Bartender', 'Bartender'),
        ('Steward', 'Steward'),
        ('Front desk', 'Front desk'),
        ('Guess services', 'Guess services'),
        ('Maintenance', 'Maintenance'),
        ('Other', _('Other')),],
        label=_("Select the jobs in which you have experience")
    )

    class Meta:
        model = Application
        fields = ['days_available_to_work','can_travel','can_work_nights','desired_job','desired_payment','position_to_apply','worked_for_this_company_before','start_date_worked_for_this_company','end_date_worked_for_this_company','has_been_convicted_of_a_felony','felony_details','can_background_check',
        'test_controlled_substances','experience_jobs','english_level','studies','specialty_of_studies','military_service','service_branch','start_period_service','end_period_service','duties_training_service']
        labels = {
            'days_available_to_work':_('Days available to work'),
            'can_travel':_('If the job requires it, can you travel?'),
            'can_work_nights':_('Can you work nights?'),
            'desired_job':_("Desired job"),
            'desired_payment':_("Desired pay per hour"),
            'position_to_apply':_('Position to which applies'),
            'worked_for_this_company_before':_('Have you worked for this company before?'),
            'start_date_worked_for_this_company':_('Start date MONTH/DAY/YEAR'),
            'end_date_worked_for_this_company':_('End date MONTH/DAY/YEAR'),
            'has_been_convicted_of_a_felony':_('Have you ever been convicted of a felony?'),
            'felony_details': _('Describe the details of the crime for which you were convicted'),
            'can_background_check':_('Are you open to a background check?'),
            'test_controlled_substances':_('If Hired, Are You Willing To Test For Controlled Substances?'),
            'english_level':_('English language level'),
            'studies':_('Indicate the studies you have carried out'),
            'specialty_of_studies':_('Specialty of your studies'),
            'military_service':_('Have you ever been a member of the united states armed services?'),
            'service_branch':_('Enter the branch in which you performed your military service'),
            'start_period_service':_('Start date MONTH/DAY/YEAR'),
            'end_period_service':_('End date MONTH/DAY/YEAR'),
            'duties_training_service':_('Describe your duties and any special training')

        }
        
        widgets = {
            'experience_jobs': forms.CheckboxSelectMultiple
        }
    
    def clean(self):
        cleaned_data = super().clean()
        for field in cleaned_data:
            
            try:
                #Eliminamos espacios en blanco
                cleaned_data[field] = cleaned_data[field].strip()
            except:
                pass

            if isinstance(cleaned_data[field], str):

                if field == "felony_details" or field == "duties_training_service" or field == "specialty_of_studies" or field == "service_branch":
                    
                    only_letters(cleaned_data[field], self.fields[field].label)
                    cleaned_data[field] = cleaned_data[field].capitalize()
                    

        return cleaned_data
    def save(self, commit=True):
        instance = super().save(commit=False)
        experience = self.cleaned_data['experience_jobs']
        instance.experience = ','.join(str(opcion) for opcion in experience)
        if commit:
            instance.save()
        return instance

class MedicalFormForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    diseases_suffered = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=[('Epilepsy', _('Epilepsy')),
        ('Diabetes', _('Diabetes')),
        ('Heart disease', _('Heart disease')),
        ('Hyperinsulinism', _('Hyperinsulinism')),
        ('Thrombopheblitis', _('Thrombopheblitis')),
        ('Total deafness', _('Total deafness')),
        ('Hemophilia', _('Hemophilia')),
        ('Polio', _('Polio')),
        ('Herniated vertebral disc', _('Herniated vertebral disc')),
        ('Multiple sclerosis', _('Multiple sclerosis')),
        ('Inflammation of the bones', _('Inflammation of the bones')),
        ('Inflammation of the joint cartilage', _('Inflammation of the joint cartilage')),
        ('Amputation of, feet, leg, arm, hand..', _('Amputation of, feet, leg, arm, hand..')),
        ('Total or partial loss of vision', _('Total or partial loss of vision')),
        ('One spinal disc removed',_('One spinal disc removed')),
        ('Any back or neck injury',_('Any back or neck injury')),
        ('Knee ligament fracture',_('Knee ligament fracture')),
        ('Parkinson''s disease',_('Parkinson''s disease')),
        ('Cerebral palsy',_('Cerebral palsy')),
        ('Muscular dystrophy',_('Muscular dystrophy')),
        ('Other',_('Other')),
        ('None',_('None'))],
        label= _('Select the diseases you suffer from')
    )

    class Meta:
        model = MedicalForm
        fields = ['height', 'weight', 'allergic_to', 'diseases_suffered', 'received_workers_compensation','workers_compensation_details', 'received_surgery_for_fracture','fracture_details','physical_disability_evaluation','physical_disability_details']
        labels = {
            'height':_('Enter your height in feet'),
            'weight':_('Enter your weight in pounds'),
            'allergic_to':_('Mention any allergies you have'),
            'received_workers_compensation':_('Have you ever received workers compensation due to an injury at work?'),
            'workers_compensation_details': _('Explain why you have received workers\' compensation'),
            'received_surgery_for_fracture':_('Have you received surgery for a fracture?'),
            'fracture_details': _('Describe the details of your fracture'),
            'physical_disability_evaluation':_('Have you received any type of physical disability evaluation assigned by any insurance company or state or federal agency?'),
            'physical_disability_details': _('Describe the details of the physical disability evaluation')
        }
    
    # physical_disability_evaluation = forms.CharField(label=_('Have you received any kind of physical disability evaluation or assigned by any insurance company or state/or federal agency? If the answer is yes, describe why, when and where'))
    widgets = {
            'diseases_suffered': forms.CheckboxSelectMultiple
        }
    
    def clean(self):
        cleaned_data = super().clean()
        for field in cleaned_data:
            
            try:
                #Eliminamos espacios en blanco
                cleaned_data[field] = cleaned_data[field].strip()
            except:
                pass

            if isinstance(cleaned_data[field], str):

                if field == "allergic_to" or field == "workers_compensation_details" or field == "fracture_details" or field == "physical_disability_details":
                    
                    only_letters(cleaned_data[field], self.fields[field].label)
                    cleaned_data[field] = cleaned_data[field].capitalize()
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        diseases_suffered = self.cleaned_data['diseases_suffered']
        instance.diseases_suffered = ','.join(str(opcion) for opcion in diseases_suffered)
        if commit:
            instance.save()
        return instance

class EmergencyContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = Emergency_contact
        fields = ['name', 'phone_number', 'relationship']
        labels = {'name': _('Name'),
                  'phone_number':_('Phone number'),
                  'relationship':_('Relationship')
                  }
        
    def clean(self):
        cleaned_data = super().clean()
        for field in cleaned_data:
            try:
                #Eliminamos espacios en blanco
                cleaned_data[field] = cleaned_data[field].strip()
            except:
                pass

            if isinstance(cleaned_data[field], str):

                cleaned_data[field] = cleaned_data[field].title()
        return cleaned_data

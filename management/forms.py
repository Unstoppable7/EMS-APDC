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
                    only_letters(cleaned_data[field])

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
        self.helper.attrs['autocomplete'] = 'nope'
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
        
        state = State.objects.filter(name=state_name_formatted).first()
        if(state is None):
            
            raise forms.ValidationError(_("Please enter a valid state."))
        return state
    
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
                    only_letters(cleaned_data[field])

        return cleaned_data
    
    def save(self, commit=True):
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
    
    DESIRED_JOB_CHOICES = [
        ('Full Time', _('Full Time')),
        ('Part Time', _('Part Time')),
        ('Seasonal', _('Seasonal')),
    ]

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
        fields = ['days_available_to_work','can_travel','can_work_nights','desired_job','desired_payment','position_to_apply','worked_for_this_company_before','has_been_convicted_of_a_felony','can_background_check',
        'test_controlled_substances','experience_jobs','english_level','studies','specialty_of_studies','military_service','service_branch','start_period_service','end_period_service','duties_training_service']
        labels = {
            'days_available_to_work':_('Days available to work'),
            'can_travel':_('If the job requires it, can you travel?'),
            'can_work_nights':_('Can you work nights?'),
            'position_to_apply':_('Position to which applies'),
            'can_background_check':_('Are you open to a background check?'),
            'english_level':_('English language level'),'studies':_('Indicate the studies you have carried out'),
            'specialty_of_studies':_('Specialty of your studies'),'military_service':_('Have you ever been a member of the united states armed services?'),
        }
        
        widgets = {
            'experience_jobs': forms.CheckboxSelectMultiple
        }

    ##Manejar en el HTML
    service_branch = forms.CharField(required=False, label=_('Enter the branch in which you performed your military service (if apply)'))
    start_period_service = forms.DateField(required=False,label=_('Military service start date (if apply)'))
    end_period_service = forms.DateField(required=False,label=_('Military service end date (if apply)'))
    duties_training_service = forms.CharField(label=_('Describe your duties and any special training (if apply)'),required=False)

    worked_for_this_company_before = forms.CharField(label=_('Have you worked for this company before?. If the answer is yes, indicate the start date and end date'))
    has_been_convicted_of_a_felony = forms.CharField(label=_('Have you ever been convicted of a felony?. If the answer is yes, explain'))
    #test_controlled_substances = forms.BooleanField(label=_('If Hired, Are You Willing To Test For Controlled Substances?'))
    test_controlled_substances = forms.TypedChoiceField(label=_('If Hired, Are You Willing To Test For Controlled Substances?'),coerce=lambda x: x =='True', choices=((True, _('Yes')), (False, _('No'))))
    desired_job = forms.ChoiceField(choices=DESIRED_JOB_CHOICES, label=_("Desired job"))
    desired_payment = forms.CharField(label=_("Desired payment"))

    def clean(self):
        cleaned_data = super().clean()
        for field in cleaned_data:
            
            try:
                #Eliminamos espacios en blanco
                cleaned_data[field] = cleaned_data[field].strip()
            except:
                pass
            if isinstance(cleaned_data[field], str):
                only_letters(cleaned_data[field])
                cleaned_data[field] = cleaned_data[field].title()
                    
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
        fields = ['height', 'weight', 'allergic_to', 'diseases_suffered', 'received_workers_compensation', 'received_surgery_for_fracture']
        labels = {
            'height':_('Enter your height in feet'),
            'weight':_('Enter your weight in pounds'),
            'allergic_to':_('Mention any allergies you have'),
            'received_workers_compensation':_('Have you ever received workers compensation due to an injury at work? If the answer is yes, describe why?'),
            'received_surgery_for_fracture':_('Have you received surgery for a fracture? If the answer is yes, describe all the details')
        }
    
    physical_disability_evaluation = forms.CharField(label=_('Have you received any kind of physical disability evaluation or assigned by any insurance company or state/or federal agency? If the answer is yes, describe why, when and where'))
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
                only_letters(cleaned_data[field])
                cleaned_data[field] = cleaned_data[field].title()
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

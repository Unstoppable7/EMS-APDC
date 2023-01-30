from django.contrib import admin
from .models import Location,Department,Employee,EmployeeInterview, Application, Emergency_contact, Document, MedicalForm, EmployeeByCoordinator, Employee_head, Employee_job, Job,EmployeeOpen
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html

from django.shortcuts import redirect
from django.urls import path

from django.db.models import Q

#Tabular inline models

class ApplicationInline(admin.StackedInline): 
   model= Application 
   fields = ['days_available_to_work', 'can_travel', 'can_work_nights', 'can_background_check', 'position_to_apply', 'experience', 'english_level', 'studies', 'military_service']
   extra = 1

class MedicalFormInline(admin.StackedInline): 
   model= MedicalForm 
   fields = ['height', 'weight', 'allergic_to', 'diseases_suffered', 'received_workers_compensation',
   'received_surgery_for_fracture']
   extra = 1

class Emergency_contactInline(admin.StackedInline): 
   model= Emergency_contact 
   fields = ['name', 'phone_number', 'relationship']
   extra = 1

class DocumentInline(admin.StackedInline): 
   model= Document 
   fields = ['type', 'date_of_expiration', 'file']
   extra = 1

class Employee_jobInline(admin.StackedInline): 
   model= Employee_job 
   fields = ['employee', 'job']
   extra = 1
#END tabular inline models

#CustomFilters

class ExperienceListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = ('Experience')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'experience'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [('Manager', 'Manager'),
        ('Housekeeping', 'Housekeeping'),
        ('Houseman', 'Houseman'),
        ('Community Areas', 'Community Areas'),
        ('Supervisor', 'Supervisor'),
        ('Inspector', 'Inspector'),
        ('Cook', 'Cook'),
        ('Precook', 'Precook'),
        ('Bartender', 'Bartender'),
        ('Steward', 'Steward'),
        ('Front desk', 'Front desk'),
        ('Guess services', 'Guess services'),
        ('Maintenance', 'Maintenance'),
        ('Other', 'Other'),]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if not self.value() == None:
            return queryset.filter(application_employee__experience__icontains=self.value())

class EnglishLevelListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = ('English Level')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'English_level'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [
        ('None', 'None'),
        ('Basic', 'Basic'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Fluent', 'Fluent')
        ]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if not self.value() == None:
            return queryset.filter(application_employee__english_level=self.value())

class CanTravelListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = ('Can Travel')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'Can_travel'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [
        ('true', 'Yes'),
        ('false', 'No'),
        ]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'true':
            return queryset.filter(application_employee__can_travel=True)
        if self.value() == 'false':
            return queryset.filter(application_employee__can_travel=False)

class CanWorkNightListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = ('Can Work Night')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'can_work_night'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [
        ('true', 'Yes'),
        ('false', 'No'),
        ]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'true':
            return queryset.filter(application_employee__can_work_nights=True)
        if self.value() == 'false':
            return queryset.filter(application_employee__can_work_nights=False)

#END customFilters

@admin.register(Employee) 
class EmployeeAdmin(admin.ModelAdmin): 
    fields=('type', 'status', 'name', 'last_name', 'phone_number', 'mail', 'date_of_birth', 
    'address','city','zip_code') 
    inlines=[ApplicationInline,Employee_jobInline,MedicalFormInline,Emergency_contactInline,DocumentInline]

    list_display = ['id', 'status', 'type', 'full_name', 'phone_number', 'date_of_birth',
    'get_job_name','get_head','date_created', 'updated_at']
    list_filter = ['type', 'status', 'date_created', 'updated_at']
    search_fields = ['name', 'last_name', 'status']

    #Propiedad que me dice que campos tendran el link que lleva a editar
    list_display_links = ('full_name',)
    
    #Propiedad que me permite editar este campo desde la vista principal, no debe ser aparecer en list_display_links y debe aparecer en list_display
    #list_editable = ('status',)

    # @admin.display(ordering='job__department__location__name')
    # def get_location(self, obj):
    #     return obj.job.department.location
    # get_location.short_description = 'location'

    #@admin.display(ordering='job__name')
    def get_job_name(self, obj):
        jobs = []
        for employee_job in Employee_job.objects.filter(employee=obj):

            jobs.append(str(employee_job.job))
        
        if not jobs:
            return '-'
        return ','.join(jobs)
    get_job_name.short_description = 'Jobs'

    #@admin.display(ordering='head__full_name')
    def get_head(self, obj):
        heads = []
        for employee_head in Employee_head.objects.filter(employee=obj):

            heads.append(str(employee_head.head.full_name))
        
        if not heads:
            return '-'
        return ','.join(heads)
    get_head.short_description = 'manager'

@admin.register(EmployeeInterview) 
class EmployeeAdminInterview(admin.ModelAdmin): 
    fields=('type', 'status', 'name', 'last_name', 'phone_number', 'mail', 'date_of_birth', 
    'address','city','zip_code') 
    inlines=[ApplicationInline,Employee_jobInline,MedicalFormInline,Emergency_contactInline,DocumentInline]

    list_display = ['id', 'full_name', 'date_of_birth','get_application_experience',
    'get_application_english_level','get_application_can_travel','get_application_can_work_nights',
    'date_created']
    list_filter = [ExperienceListFilter,EnglishLevelListFilter,CanTravelListFilter,CanWorkNightListFilter]
    search_fields = ['name', 'last_name']
    list_display_links = ('full_name',)

    def get_queryset(self, request):
        
        qs = super().get_queryset(request)
        return qs.filter(status="Interview")

    def get_application_english_level(self, obj):
        
        application = Application.objects.filter(employee=obj.id).first()
        
        if(application == None):
            return '-'
        
        return application.english_level
    get_application_english_level.short_description = 'english_level'

    def get_application_can_travel(self, obj):
        
        application = Application.objects.filter(employee=obj.id).first()
        
        if(application == None):
            return '-'
        
        if application.can_travel:
            return 'Yes'
        else:
            return 'No'
    get_application_can_travel.short_description = 'can travel'

    def get_application_experience(self, obj):
        
        application = Application.objects.filter(employee=obj.id).first()

        if(application == None):
            return '-'
        
        return application.experience
    get_application_experience.short_description = 'experience'

    def get_application_can_work_nights(self, obj):
        
        application = Application.objects.filter(employee=obj.id).first()
        
        if(application == None):
            return '-'
        
        if application.can_work_nights:
            return 'Yes'
        else:
            return 'No'
    get_application_can_work_nights.short_description = 'can work nights'

@admin.register(EmployeeOpen) 
class EmployeeOpenAdmin(admin.ModelAdmin): 
    fields=('type', 'status', 'name', 'last_name', 'phone_number', 'mail', 'date_of_birth', 
    'address','city','zip_code') 
    inlines=[ApplicationInline,Employee_jobInline,MedicalFormInline,Emergency_contactInline,DocumentInline]

    list_display = ['id', 'full_name', 'date_of_birth','get_application_experience',
    'get_application_english_level','get_application_can_travel','get_application_can_work_nights',
    'date_created']
    list_filter = [ExperienceListFilter,EnglishLevelListFilter,CanTravelListFilter,CanWorkNightListFilter]
    search_fields = ['name', 'last_name']
    list_display_links = ('full_name',)

    def get_queryset(self, request):
        
        qs = super().get_queryset(request)
        return qs.filter(status="Open")

    def get_application_english_level(self, obj):
        
        application = Application.objects.filter(employee=obj.id).first()
        
        if(application == None):
            return '-'
        
        return application.english_level
    get_application_english_level.short_description = 'english_level'

    def get_application_can_travel(self, obj):
        
        application = Application.objects.filter(employee=obj.id).first()
        
        if(application == None):
            return '-'
        
        if application.can_travel:
            return 'Yes'
        else:
            return 'No'
    get_application_can_travel.short_description = 'can travel'

    def get_application_experience(self, obj):
        
        application = Application.objects.filter(employee=obj.id).first()

        if(application == None):
            return '-'
        
        return application.experience
    get_application_experience.short_description = 'experience'

    def get_application_can_work_nights(self, obj):
        
        application = Application.objects.filter(employee=obj.id).first()
        
        if(application == None):
            return '-'
        
        if application.can_work_nights:
            return 'Yes'
        else:
            return 'No'
    get_application_can_work_nights.short_description = 'can work nights'

@admin.register(EmployeeByCoordinator) 
class EmployeeAdminByCoordinator(admin.ModelAdmin): 

    fields=('type', 'status', 'name', 'last_name', 'phone_number', 'mail', 'date_of_birth', 
    'address','city','zip_code') 
    inlines=[ApplicationInline,Employee_jobInline,MedicalFormInline,Emergency_contactInline,DocumentInline]

    list_display = ['id', 'status', 'type', 'full_name', 'phone_number', 'date_of_birth',
    'get_job_name','date_created', 'updated_at']
    list_filter = ['type', 'status', 'date_created', 'updated_at']
    search_fields = ['name', 'last_name', 'status']

    #Propiedad que me dice que campos tendran el link que lleva a editar
    list_display_links = ('full_name',)
    
    #Propiedad que me permite editar este campo desde la vista principal, no debe ser aparecer en list_display_links y debe aparecer en list_display
    #list_editable = ('status',)

    def get_queryset(self, request):
        my_empoyees = super().get_queryset(request)
        
        try:

            head = None
            head = Employee.objects.get(mail=request.user.email)

            ## Relacion inversa atraves del parametro related_name del modelo Employee_head
            my_empoyees = super().get_queryset(request).filter(employeeWithHead__head=head)
        except:
            pass
        return my_empoyees

    def get_job_name(self, obj):
        jobs = []
        for employee_job in Employee_job.objects.filter(employee=obj):

            jobs.append(str(employee_job.job))
        
        if not jobs:
            return '-'
        return ','.join(jobs)
    get_job_name.short_description = 'Jobs'

@admin.register(Department)
class Department(admin.ModelAdmin):
    list_display = ('name','location')

admin.site.register(Location)
#admin.site.register(Employee_head)
admin.site.register(Job)

# @admin.register(Employee_job)
# class Employee_jobAdmin(admin.ModelAdmin):
#     list_display = ('employee','job')

# @admin.register(Employee_head) 
# class Employee_headAdmin(admin.ModelAdmin):

#     #inlines=[ApplicationInline,MedicalFormInline,Emergency_contactInline,DocumentInline]

#     list_display = ['get_employee_status','get_employee_type','get_employee_name','get_employee_phone_number','get_employee_date_of_birth','get_employee_address','get_employee_job','get_employee_location','get_employee_date_created','get_employee_updated_at',]
    
#     list_filter = ['employee__type', 'employee__status','employee__job','employee__job__department__location__name', 'employee__date_created', 'employee__updated_at']
#     search_fields = ['employee__name', 'employee__last_name', 'employee__status','employee__job__department__location__name']

#     def get_queryset(self, request):
#         #cambiar a filtrar por email
#         qs = super().get_queryset(request)
#         return qs.filter(head__name=request.user.first_name)

#     @admin.display(ordering='employee__address')
#     def get_employee_address(self, obj):
#         return obj.employee.address
#     get_employee_address.short_description = 'Address'


#     @admin.display(ordering='employee__updated_at')
#     def get_employee_updated_at(self, obj):
#         return obj.employee.updated_at
#     get_employee_updated_at.short_description = 'Update at'

#     @admin.display(ordering='employee__date_created')
#     def get_employee_date_created(self, obj):
#         return obj.employee.date_created
#     get_employee_date_created.short_description = 'Date created'

#     @admin.display(ordering='employee__job__department__location__name')
#     def get_employee_location(self, obj):
#         return obj.employee.job.department.location
#     get_employee_location.short_description = 'Location'

#     @admin.display(ordering='employee__job')
#     def get_employee_job(self, obj):
#         return obj.employee.job.name
#     get_employee_job.short_description = 'Job'

#     @admin.display(ordering='employee__date_of_birth')
#     def get_employee_date_of_birth(self, obj):
#         return obj.employee.date_of_birth
#     get_employee_date_of_birth.short_description = 'Date of Birth'

#     @admin.display(ordering='employee__full_name')
#     def get_employee_name(self, obj):
#         return obj.employee.full_name
#     get_employee_name.short_description = 'Full name'

#     @admin.display(ordering='employee__status')
#     def get_employee_status(self, obj):
#         return obj.employee.status
#     get_employee_status.short_description = 'Status'

#     @admin.display(ordering='employee__type')
#     def get_employee_type(self, obj):
#         return obj.employee.type
#     get_employee_type.short_description = 'Type'

#     @admin.display(ordering='employee__phone_number')
#     def get_employee_phone_number(self, obj):
#         return obj.employee.phone_number
#     get_employee_phone_number.short_description = 'Phone Number'

    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     employee_head = self.get_object(request, object_id)
    #     url = reverse('admin:%s_%s_change' % (employee_head.employee._meta.app_label, employee_head.employee._meta.model_name), args=[employee_head.employee.id])
        
    #     return redirect(url)


from django.contrib import admin
from .models import Location,Department,Employee,EmployeeInterview, Application, Emergency_contact, Document, MedicalForm, MyEmployeeSection, Employee_head, Employee_job, Job,Recruiting,ApplicationManagement,AccountingStatus,City,State,Address,Frontdesk,User
from django.contrib import messages
from django.utils.translation import ngettext
from django.db.models import Q
from django.contrib.auth.admin import UserAdmin

# Eliminar la acción de eliminación para todos los modelos
#admin.site.disable_action('delete_selected')

#Tabular inline models

class AddressInline(admin.StackedInline): 
   model= Address 
   fields = ['street', 'unit_number', 'city', 'state', 'postal_code',]
   extra = 0

class ApplicationInline(admin.StackedInline): 
   model= Application 
   fields = ['days_available_to_work', 'can_travel', 'can_work_nights', 'desired_job','desired_payment','position_to_apply','worked_for_this_company_before','start_date_worked_for_this_company','end_date_worked_for_this_company','has_been_convicted_of_a_felony','felony_details', 'can_background_check','test_controlled_substances', 'experience', 'english_level', 'studies','specialty_of_studies', 'military_service','service_branch','start_period_service','end_period_service','duties_training_service',]
   extra = 0

class MedicalFormInline(admin.StackedInline): 
   model= MedicalForm 
   fields = ['height', 'weight', 'allergic_to', 'diseases_suffered', 'received_workers_compensation','workers_compensation_details','received_surgery_for_fracture','fracture_details','physical_disability_evaluation','physical_disability_details',]
   extra = 0

class Emergency_contactInline(admin.StackedInline): 
   model= Emergency_contact 
   fields = ['name', 'phone_number', 'relationship']
   extra = 0

class DocumentInline(admin.StackedInline): 
    model= Document 
    fields = ['type', 'date_of_expiration', 'file']
    extra = 1

    #TODO agregar la condicion para evitar el acceso a las aplicaciones de southeast
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.email == 'prueba@prueba.com':
            queryset = queryset.exclude(type='Southeast')
        return queryset

class Employee_jobInline(admin.StackedInline): 
   model= Employee_job 
   fields = ['employee', 'job']
   extra = 1
   verbose_name = 'Job'
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
            
            if self.value() == 'Intermediate':
                return queryset.filter(Q(application_employee__english_level='Intermediate') | Q(application_employee__english_level='Advanced'))

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

class LocationListFilter(admin.SimpleListFilter):
    title = 'Location'
    parameter_name = 'location'

    def lookups(self, request, model_admin):
        #qs = model_admin.get_queryset(request)
        #types = qs.values_list('Location')

        #Buscar solo los nombres
        types = Location.objects.values_list('name',flat=True)

        return [(value, value) for value in types]

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        return queryset.filter(employee_job_employee__job__department__location__name=self.value())

#END customFilters

@admin.register(Employee) 
class EmployeeAdmin(admin.ModelAdmin): 
    fields=('type', 'status', 'application_status','quickbooks_status','first_name', 'last_name', 'phone_number', 'email', 'date_of_birth') 
    inlines=[AddressInline,ApplicationInline,Employee_jobInline,MedicalFormInline,Emergency_contactInline,DocumentInline]

    list_display = ['id','status', 'application_status', 'quickbooks_status','type', 'full_name', 'phone_number', 'date_of_birth','get_job_name','get_locations','get_head','date_created', 'updated_at']
    list_filter = ['type', 'status','employee_job_employee__job__department__location__name', 'date_created', 'updated_at',]
    search_fields = ['first_name', 'last_name', 'status', 'employee_job_employee__job__department__location__name']

    list_per_page = 20

    #Propiedad que me dice que campos tendran el link que lleva a editar
    #list_display_links = ('full_name',)
    #Propiedad que me permite editar este campo desde la vista principal, no debe ser aparecer en list_display_links y debe aparecer en list_display
    #list_editable = ('status',)
    #actions = ['make_active','make_open','make_inactive', 'make_do_not_hire']

    @admin.action(description='Mark as active')
    def make_active(self, request, queryset):
        updated = queryset.update(status='Active')
        
        self.message_user(request, ngettext(
            '%d employee was successfully marked as active.',
            '%d employees were successfully marked as active.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Mark as open')
    def make_open(self, request, queryset):
            
        for e in queryset:
            e.status = 'Open'
            e.save()

        self.message_user(request, ngettext(
            '%d employee was successfully marked as open.',
            '%d employees were successfully marked as open.',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)

    @admin.action(description='Mark as inactive')
    def make_inactive(self, request, queryset):
        for e in queryset:
            e.status = 'Inactive'
            e.save()

        self.message_user(request, ngettext(
            '%d employee was successfully marked as inactive.',
            '%d employees were successfully marked as inactive.',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)

    @admin.action(description='Mark as do not hire')
    def make_do_not_hire(self, request, queryset):
        for e in queryset:
            e.status = 'Do Not Hire'
            e.save()

        self.message_user(request, ngettext(
            '%d employee was successfully marked as do not hire.',
            '%d employees were successfully marked as do not hire.',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)

    #Propiedad que me permite editar este campo desde la vista principal, no debe ser aparecer en list_display_links y debe aparecer en list_display
    #list_editable = ('updated_at',)
    @admin.display(ordering='employee_job_employee__job__department__location__name')
    def get_locations(self, obj):
        locations = []
        for employee_job in Employee_job.objects.filter(employee=obj):

            locations.append(str(employee_job.job.department.location))
        
        if not locations:
            return '-'
        return ','.join(locations)
    get_locations.short_description = 'Location'

    @admin.display(ordering='employee_job_employee__job__name')
    def get_job_name(self, obj):
        jobs = []
        for employee_job in Employee_job.objects.filter(employee=obj):

            jobs.append(str(employee_job.job.name).capitalize())
        
        if not jobs:
            return '-'
        return ','.join(jobs)
    get_job_name.short_description = 'Jobs'

    @admin.display(ordering='employeeWithHead__head__first_name')
    def get_head(self, obj):
        heads = []
        for employee_head in Employee_head.objects.filter(employee=obj):

            heads.append(str(employee_head.head.full_name).capitalize())
        
        if not heads:
            return '-'
        return ','.join(heads)
    get_head.short_description = 'manager'

@admin.register(EmployeeInterview) 
class EmployeeAdminInterview(admin.ModelAdmin): 
    fields=('first_name', 'last_name', 'phone_number', 'email', 'date_of_birth') 
    inlines=[AddressInline,ApplicationInline,Employee_jobInline,MedicalFormInline,Emergency_contactInline,DocumentInline]

    list_display = ['full_name','phone_number','get_address', 'date_of_birth','get_application_experience',
    'get_application_english_level','get_application_can_travel','get_application_can_work_nights',]
    list_filter = [ExperienceListFilter,EnglishLevelListFilter,CanTravelListFilter,CanWorkNightListFilter]
    search_fields = ['first_name', 'last_name']
    list_display_links = ('full_name',)

    list_per_page = 20

    #Propiedad que me permite editar este campo desde la vista principal, no debe ser aparecer en list_display_links y debe aparecer en list_display
    #list_editable = ('status',)
    actions = ['make_no_application_open','make_do_not_hire']

    # @admin.action(description='Mark as active')
    # def make_active(self, request, queryset):
    #     updated = queryset.update(status='Active')
    #     self.message_user(request, ngettext(
    #         '%d employee was successfully marked as active.',
    #         '%d employees were successfully marked as active.',
    #         updated,
    #     ) % updated, messages.SUCCESS)

    @admin.display(ordering='employee_address_employee')
    def get_address(self, obj):
        if obj.employee_address_employee.first() is not None:
        
            return str(obj.employee_address_employee.first())
        else: return "-"
    get_address.short_description = 'Address'

    @admin.action(description='Mark to open and change to no application')
    def make_no_application_open(self, request, queryset):
            
        for e in queryset:
            e.application_status = 'No Application'
            e.status = 'Open'
            e.save()

        self.message_user(request, ngettext(
            '%d employee was successfully mark to Open and application status changed to No Application.',
            '%d employees were successfully mark to Open and application status changed to No Application.',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)

    @admin.action(description='Mark as do not hire')
    def make_do_not_hire(self, request, queryset):
        for e in queryset:
            e.status = 'Do Not Hire'
            e.save()

        self.message_user(request, ngettext(
            '%d employee was successfully marked as do not hire.',
            '%d employees were successfully marked as do not hire.',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)

    def get_queryset(self, request):
        
        qs = super().get_queryset(request)
        return qs.filter(status="Undefined")

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

@admin.register(Recruiting) 
class RecruitingAdmin(admin.ModelAdmin): 
    fields=('first_name', 'last_name', 'phone_number', 'email','date_of_birth') 
    inlines=[AddressInline,ApplicationInline,MedicalFormInline,Emergency_contactInline,DocumentInline]

    list_display = ['full_name','get_address','phone_number','date_of_birth','get_application_experience',
    'get_application_english_level','get_application_can_travel','get_application_can_work_nights', 'application_status',
    ]
    list_filter = [ExperienceListFilter,EnglishLevelListFilter,CanTravelListFilter,CanWorkNightListFilter]
    search_fields = ['first_name', 'last_name']
    list_display_links = ('full_name',)
    #Propiedad que me permite editar este campo desde la vista principal, no debe ser aparecer en list_display_links y debe aparecer en list_display
    #list_editable = ('status',)

    list_per_page = 20

    actions = ['make_stand_by','make_do_not_hire']

    @admin.display(ordering='employee_address_employee')
    def get_address(self, obj):
        if obj.employee_address_employee.first() is not None:
        
            return str(obj.employee_address_employee.first())
        else: return "-"
    get_address.short_description = 'Address'

    @admin.action(description='Mark as stand by')
    def make_stand_by(self, request, queryset):
        
        #coordinator = Employee.objects.filter(Q(email=request.user.email) & Q(employee_job_employee__job__name='Coordinator')).first()

        coordinator = request.user.employee

        if coordinator is not None:
            for e in queryset:

                e.status = 'Stand By'
                Employee_head.objects.create(employee=e, head=coordinator)
                e.save()

            self.message_user(request, ngettext(
                '%d employee was successfully marked as "stand by" and added to the "my employees" section.',
                '%d employees were successfully marked as "stand by" and added to the "my employees" section.',
                queryset.count(),
            ) % queryset.count(), messages.SUCCESS)
        else:
            self.message_user(request, ngettext(
                "%d employee could not be marked as \"stand by\" and was not added to the \"my employees\" section. \nThere is a problem with your user",
                '%d employees could not be marked as "stand by" and were not added to the "my employees" section. \nThere is a problem with your user',
                queryset.count(),
            ) % queryset.count(), messages.ERROR)
            
    @admin.action(description='Mark as active')
    def make_active(self, request, queryset):
        updated = queryset.update(status='Active')
        self.message_user(request, ngettext(
            '%d employee was successfully marked as active.',
            '%d employees were successfully marked as active.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Mark as do not hire')
    def make_do_not_hire(self, request, queryset):
        for e in queryset:
            e.status = 'Do Not Hire'
            e.save()

        self.message_user(request, ngettext(
            '%d employee was successfully marked as do not hire.',
            '%d employees were successfully marked as do not hire.',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)

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

@admin.register(MyEmployeeSection) 
class EmployeeAdminByCoordinator(admin.ModelAdmin): 

    fields=('first_name', 'last_name', 'phone_number', 'email', 'date_of_birth') 
    inlines=[AddressInline,ApplicationInline,Employee_jobInline,MedicalFormInline,Emergency_contactInline,DocumentInline]

    list_display = ['id', 'full_name','status', 'application_status','phone_number', 'get_address','get_job_name', 'get_locations']
    list_filter = ['type', 'status', 'employee_job_employee__job__department__location__name', 'date_created', 'updated_at']
    search_fields = ['first_name', 'last_name', 'status','employee_job_employee__job__department__location__name']

    #Propiedad que me dice que campos tendran el link que lleva a editar
    list_display_links = ('full_name',)
    #Propiedad que me permite editar este campo desde la vista principal, no debe ser aparecer en list_display_links y debe aparecer en list_display
    #list_editable = ('status',)
    
    list_per_page = 20

    actions = ['make_open','make_inactive','make_do_not_hire']

    @admin.display(ordering='employee_address_employee')
    def get_address(self, obj):
        if obj.employee_address_employee.first() is not None:
        
            return str(obj.employee_address_employee.first())
        else: return "-"
    get_address.short_description = 'Address'

    @admin.action(description='Mark as open')
    def make_open(self, request, queryset):
            
        for e in queryset:
            e.status = 'Open'
            e.save()

        self.message_user(request, ngettext(
            '%d employee was successfully marked as open.',
            '%d employees were successfully marked as open.',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)

    @admin.action(description='Mark as inactive')
    def make_inactive(self, request, queryset):
        for e in queryset:
            e.status = 'Inactive'
            e.save()

        self.message_user(request, ngettext(
            '%d employee was successfully marked as inactive.',
            '%d employees were successfully marked as inactive.',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)

    @admin.action(description='Mark as do not hire')
    def make_do_not_hire(self, request, queryset):
        for e in queryset:
            e.status = 'Do Not Hire'
            e.save()

        self.message_user(request, ngettext(
            '%d employee was successfully marked as do not hire.',
            '%d employees were successfully marked as do not hire.',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)

    def get_queryset(self, request):
        my_employees = super().get_queryset(request)
        
        try:
            head = None
            #head = Employee.objects.filter(email=request.user.email).first()
            head = request.user.employee
            if head is not None:
                my_employees = super().get_queryset(request).filter(employeeWithHead__head=head)
            ## Relacion inversa atraves del parametro related_name del modelo Employee_head
        except:
            pass
        return my_employees

    @admin.display(ordering='employee_job_employee__job__department__location__name')
    def get_locations(self, obj):
        locations = []
        for employee_job in Employee_job.objects.filter(employee=obj):

            locations.append(str(employee_job.job.department.location).capitalize())
        
        if not locations:
            return '-'
        return ','.join(locations)
    get_locations.short_description = 'Location'

    @admin.display(ordering='employee_job_employee__job__name')
    def get_job_name(self, obj):
        jobs = []
        for employee_job in Employee_job.objects.filter(employee=obj):

            jobs.append(str(employee_job.job.name).capitalize())
        
        if not jobs:
            return '-'
        return ','.join(jobs)
    get_job_name.short_description = 'Jobs'

@admin.register(ApplicationManagement)
class ApplicationManagementAdmin(admin.ModelAdmin):
    fields=('type', 'status', 'application_status', 'first_name', 'last_name', 'phone_number', 'email', 'date_of_birth') 
    inlines=[AddressInline,ApplicationInline,Employee_jobInline,MedicalFormInline,Emergency_contactInline,DocumentInline]
    list_display = ['application_status','id','full_name','status', 'get_job_name','get_locations','get_head', 'date_created']
    #list_editable = ('status','application_status')
    list_per_page = 10
    list_filter = ['employee_job_employee__job__department__location__name']
    search_fields = ['first_name', 'last_name', 'employee_job_employee__job__department__location__name']
    #list_display_links = ('full_name',)
    actions = ['make_no_application_open','make_frontdesk','make_human_resources']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        
        queryset = super().get_queryset(request).filter(Q(application_status='Undefined') | Q(application_status='Frontdesk') | Q(application_status='Human Resources') | Q(application_status='Pending'))
        
        return queryset

    @admin.action(description='Mark to open and change to no application')
    def make_no_application_open(self, request, queryset):
            
        for e in queryset:
            e.application_status = 'No Application'
            e.status = 'Open'
            e.save()

        self.message_user(request, ngettext(
            '%d employee was successfully mark to Open and application status changed to No Application.',
            '%d employees were successfully mark to Open and application status changed to No Application.',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)

    @admin.action(description='Change to regular application')
    def make_regular_application(self, request, queryset):
            
        for e in queryset:
            e.application_status = 'Regular Application'
            e.save()

        self.message_user(request, ngettext(
            '%d application status was successfully changed to Regular Application.',
            '%d applications status were successfully changed to Regular Application.',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)
    
    @admin.action(description='Change to southeast')
    def make_southeast(self, request, queryset):
            
        for e in queryset:
            e.application_status = 'Southeast'
            e.save()

        self.message_user(request, ngettext(
            '%d application status was successfully changed to Southeast.',
            '%d applications status was successfully changed to Southeast.',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)

    @admin.action(description='Change to human resources')
    def make_human_resources(self, request, queryset):
            
        for e in queryset:
            e.application_status = 'Human Resources'
            e.save()

        self.message_user(request, ngettext(
            '%d application status was successfully changed to Human Resources.',
            '%d applications status was successfully changed to Human Resources.',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)

    @admin.action(description='Change to frontdesk')
    def make_frontdesk(self, request, queryset):
            
        for e in queryset:
            e.application_status = 'Frontdesk'
            e.save()

        self.message_user(request, ngettext(
            '%d application status was successfully changed to Frontdesk.',
            '%d applications status was successfully changed to Frontdesk.',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)

    @admin.display(ordering='employee_job_employee__job__department__location__name')
    def get_locations(self, obj):
        locations = []
        for employee_job in Employee_job.objects.filter(employee=obj):

            locations.append(str(employee_job.job.department.location).capitalize())
        
        if not locations:
            return '-'
        return ','.join(locations)
    get_locations.short_description = 'Location'

    @admin.display(ordering='employee_job_employee__job__name')
    def get_job_name(self, obj):
        jobs = []
        for employee_job in Employee_job.objects.filter(employee=obj):

            jobs.append(str(employee_job.job.name).capitalize())
        
        if not jobs:
            return '-'
        return ','.join(jobs)
    get_job_name.short_description = 'Jobs'

    @admin.display(ordering='employeeWithHead__head__first_name')
    def get_head(self, obj):
        heads = []
        for employee_head in Employee_head.objects.filter(employee=obj):

            heads.append(str(employee_head.head.full_name).capitalize())
        
        if not heads:
            return '-'
        return ','.join(heads)
    get_head.short_description = 'manager'

@admin.register(AccountingStatus) 
class EmployeeAdminAccountingStatus(admin.ModelAdmin): 

    fields=('type','quickbooks_status','first_name', 'last_name', 'phone_number', 'email', 'date_of_birth') 
    #'address','city','zip_code') 
    inlines=[AddressInline]

    list_display = ['quickbooks_status','id', 'full_name','get_address', 'phone_number','date_of_birth','type', 'get_job_name','get_locations','get_head','updated_at']
    
    list_filter = ['quickbooks_status', 'employee_job_employee__job__department__location__name']
    search_fields = ['id','first_name', 'last_name','employee_job_employee__job__department__location__name']

    #Propiedad que me dice que campos tendran el link que lleva a editar
    #list_display_links = ('full_name',)
    #Propiedad que me permite editar este campo desde la vista principal, no debe ser aparecer en list_display_links y debe aparecer en list_display
    #list_editable = ('status',)
    
    list_per_page = 20
    actions = ['make_ready']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = super().get_queryset(request).exclude(quickbooks_status__in=['Ready', 'Not Hired'])
        queryset = queryset.prefetch_related('employee_address_employee')

        # try:
        #     head = None
        #     head = Employee.objects.filter(email=request.user.email).first()

        #     ## Relacion inversa atraves del parametro related_name del modelo Employee_head
        #     my_empoyees = super().get_queryset(request).filter(employeeWithHead__head=head)
        # except:
        #     pass

        return queryset

    # @admin.display(ordering='city_state__state')
    # def get_state(self, obj):
    #     return str(obj.city.state).capitalize()
    # get_state.short_description = 'State'

    @admin.display(ordering='employee_address_employee')
    def get_address(self, obj):
        if obj.employee_address_employee.first() is not None:
        
            return str(obj.employee_address_employee.first())
        else: return "-"
    get_address.short_description = 'Address'

    @admin.display(ordering='employee_job_employee__job__department__location__name')
    def get_locations(self, obj):
        locations = []
        for employee_job in Employee_job.objects.filter(employee=obj):

            locations.append(str(employee_job.job.department.location).capitalize())
        
        if not locations:
            return '-'
        return ','.join(locations)
    get_locations.short_description = 'Location'

    @admin.display(ordering='employee_job_employee__job__name')
    def get_job_name(self, obj):
        jobs = []
        for employee_job in Employee_job.objects.filter(employee=obj):

            jobs.append(str(employee_job.job.name).capitalize())
        
        if not jobs:
            return '-'
        return ','.join(jobs)
    get_job_name.short_description = 'Jobs'

    @admin.display(ordering='employeeWithHead__head__first_name')
    def get_head(self, obj):
        heads = []
        for employee_head in Employee_head.objects.filter(employee=obj):

            heads.append(str(employee_head.head.full_name).capitalize())
        
        if not heads:
            return '-'
        return ','.join(heads)
    get_head.short_description = 'Manager'

    @admin.action(description='Mark as ready')
    def make_ready(self, request, queryset):
            
        for e in queryset:
            e.quickbooks_status = 'Ready'
            e.save()

        self.message_user(request, ngettext(
            '%d employee was successfully marked as ready.',
            '%d employees were successfully marked as ready.',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)

    @admin.action(description='Mark as Not Hired')
    def make_not_hired(self, request, queryset):
            
        for e in queryset:
            e.quickbooks_status = 'Not Hired'
            e.save()

        self.message_user(request, ngettext(
            '%d employee was successfully marked as Not Hired.',
            '%d employees were successfully marked as Not Hired.',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)

    # @admin.action(description='Mark as inactive')
    # def make_inactive(self, request, queryset):
    #     for e in queryset:
    #         e.status = 'Inactive'
    #         e.save()

    #     self.message_user(request, ngettext(
    #         '%d employee was successfully marked as inactive.',
    #         '%d employees were successfully marked as inactive.',
    #         queryset.count(),
    #     ) % queryset.count(), messages.SUCCESS)

    # @admin.action(description='Mark as do not hire')
    # def make_do_not_hire(self, request, queryset):
    #     for e in queryset:
    #         e.status = 'Do Not Hire'
    #         e.save()

    #     self.message_user(request, ngettext(
    #         '%d employee was successfully marked as do not hire.',
    #         '%d employees were successfully marked as do not hire.',
    #         queryset.count(),
    #     ) % queryset.count(), messages.SUCCESS)

@admin.register(Frontdesk) 
class FrontdeskAdmin(admin.ModelAdmin): 
    fields=('first_name', 'last_name', 'phone_number', 'email', 'date_of_birth') 
    inlines=[AddressInline,ApplicationInline,Employee_jobInline,MedicalFormInline,Emergency_contactInline,DocumentInline]

    list_display = ['id','status', 'application_status', 'full_name', 'phone_number','get_address', 'date_of_birth','date_created', 'updated_at']
    list_filter = ['status', 'date_created', 'updated_at',]
    search_fields = ['first_name', 'last_name', 'status',]

    list_per_page = 20

    #Propiedad que me dice que campos tendran el link que lleva a editar
    #list_display_links = ('full_name',)
    #Propiedad que me permite editar este campo desde la vista principal, no debe ser aparecer en list_display_links y debe aparecer en list_display
    #list_editable = ('status',)
    actions = ['make_no_application_open']

    def get_queryset(self, request):
        
        qs = super().get_queryset(request)
        return qs.filter(Q(application_status='Undefined') | Q(application_status='Frontdesk') | Q(status='Undefined'))

    @admin.display(ordering='employee_address_employee')
    def get_address(self, obj):
        if obj.employee_address_employee.first() is not None:
        
            return str(obj.employee_address_employee.first())
        else: return "-"
    get_address.short_description = 'Address'

    @admin.action(description='Mark to open and change to no application')
    def make_no_application_open(self, request, queryset):
            
        for e in queryset:
            e.application_status = 'No Application'
            e.status = 'Open'
            e.save()

        self.message_user(request, ngettext(
            '%d employee was successfully mark to Open and application status changed to No Application.',
            '%d employees were successfully mark to Open and application status changed to No Application.',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)

    @admin.action(description='Mark as do not hire')
    def make_do_not_hire(self, request, queryset):
        for e in queryset:
            e.status = 'Do Not Hire'
            e.save()

        self.message_user(request, ngettext(
            '%d employee was successfully marked as do not hire.',
            '%d employees were successfully marked as do not hire.',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)

@admin.register(User)   
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'employee', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password','employee')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','password1', 'password2', 'is_staff','employee'),
        }),
    )
@admin.register(Department)
class Department(admin.ModelAdmin):
    list_display = ('id','name','location')
    list_per_page = 20

@admin.register(Job)
class Job(admin.ModelAdmin):
    list_display = ('id','name','department','get_location')
    list_per_page = 20

    @admin.display(ordering='department__location')
    def get_location(self,obj):
        return obj.department.location
    get_location.short_description = 'Location'


admin.site.register(City)
admin.site.register(State)
admin.site.register(Location)

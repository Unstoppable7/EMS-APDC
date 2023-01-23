from django.contrib import admin
from .models import Location,Department,Job,Employee,EmployeeInterview, Application, Emergency_contact, Document, MedicalForm, EmployeeByCoordinator, Employee_head
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html

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

#END tabular inline models

@admin.register(Employee) 
class EmployeeAdmin(admin.ModelAdmin): 
    fields=('type', 'status', 'name', 'last_name', 'phone_number', 'mail', 'date_of_birth', 
    'address','city','zip_code', 'job') 
    inlines=[ApplicationInline,MedicalFormInline,Emergency_contactInline,DocumentInline]

    list_display = ['id', 'status', 'type', 'full_name', 'phone_number', 'date_of_birth',
    'job','get_location','get_head','date_created', 'updated_at']
    list_filter = ['type', 'status', 'date_created', 'updated_at']
    search_fields = ['name', 'last_name', 'status']

    #TODO buscar como puedo poner en list_display este join o este tipo de variables
    def get_location(self, obj):
        return obj.job.department.location
    get_location.short_description = 'location'

    def get_head(self, obj):

        # location = obj.job.department.location
        # employee = Employee.objects.select_related("job__department__location").filter(job__department__location__id=location.id, job__name="Coordinator").values()
        # print(employee)

        try:
            employeeHead = Employee_head.objects.get(employee=obj)
        except:
            return '-'

        head = employeeHead.head
        
        return head.full_name
    get_head.short_description = 'manager'

@admin.register(EmployeeInterview) 
class EmployeeAdminInterview(admin.ModelAdmin): 
    fields=('type', 'status', 'name', 'last_name', 'phone_number', 'mail', 'date_of_birth', 
    'address','city','zip_code', 'job') 
    inlines=[ApplicationInline,MedicalFormInline,Emergency_contactInline,DocumentInline]

    list_display = ['id', 'full_name', 'date_of_birth','get_application_experience',
    'get_application_english_level','get_application_can_travel','get_application_can_work_nights',
    'date_created']
    list_filter = ['date_created']
    search_fields = ['name', 'last_name']

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

@admin.register(EmployeeByCoordinator) 
class EmployeeAdminByCoordinator(admin.ModelAdmin): 

    fields=('type', 'status', 'name', 'last_name', 'phone_number', 'mail', 'date_of_birth', 
    'address','city','zip_code', 'job') 
    inlines=[ApplicationInline,MedicalFormInline,Emergency_contactInline,DocumentInline]

# def view_application(self, obj):
#     url = (
#         reverse("admin:mainApp_application_changelist")
#         + "?"
#         + urlencode({"employee__id": f"{obj.id}"})
#     )
#     return format_html('<a href="{}">Details</a>', url)

# view_application.short_description = "Application"



# class StateAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name']
#     list_filter = ['name']
#     search_fields = ['name']

# class CityAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'state']
#     list_filter = ['name', 'state']
#     search_fields = ['name']

# class LocationAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'address', 'phone_number', 'zip_code', 'city']
#     list_filter = ['name', 'address', 'phone_number', 'zip_code', 'city']
#     search_fields = ['name']

# class DepartmentAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'location']
#     list_filter = ['name', 'location']
#     search_fields = ['name']

# class JobAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'department']
#     list_filter = ['name', 'department']
#     search_fields = ['name']

# class EmployeeAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'last_name', 'mail', 'type', 'status', 'date_created', 'updated_at']
#     list_filter = ['type', 'status', 'date_created', 'updated_at']
#     search_fields = ['name', 'last_name', 'mail', 'status']

# class ApplicationAdmin(admin.ModelAdmin):
#     list_display = ['employee','id', 'days_available_to_work', 'can_travel', 'can_work_nights', 'can_background_check', 'position_to_apply', 'experience', 'english_level', 'studies', 'military_service', 'file']
#     list_filter = ['days_available_to_work', 'can_travel', 'can_work_nights', 'can_background_check', 'position_to_apply', 'experience', 'english_level', 'studies', 'military_service']
#     search_fields = ['employee__name', 'employee__last_name']

# class EmergencyContactAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'phone_number', 'relationship', 'employee']
#     list_filter = ['relationship']
#     search_fields = ['employee__name', 'employee__last_name']

# class DocumentAdmin(admin.ModelAdmin):
#     list_display = ['id', 'type', 'number', 'date_of_expiration', 'file', 'employee']
#     list_filter = ['type', 'date_of_expiration']
#     search_fields = ['employee__name', 'employee__last_name']

# class MedicalFormAdmin(admin.ModelAdmin):
#     list_display = ['height', 'weight', 'allergic_to', 'diseases_suffered', 'received_workers_compensation', 'received_surgery_for_fracture']
#     search_fields = ['name']

# class TransactionAdmin(admin.ModelAdmin):
#     list_display = ['Reference', 'Start_date', 'End_date', 'Regular_hours', 'Regular_rate', 'Overtime_hours', 'Overtime_rate', 'Total_hours', 'Subtotal', 'Extra', 'Total_gross', 'Status', 'Payment_date', 'Withdrawn_date']
#     search_fields = ['name']

# class JobHistoryAdmin(admin.ModelAdmin):
#     list_display = ['start_date', 'end_date']
#     search_fields = ['name']

# @admin.register(Application) 
# class ApplicationAdmin(admin.ModelAdmin): 
#     # fields=('experience','english_level', 'can_travel', 'can_work_nights', 'studies', 'days_available_to_work', 'can_background_check', 
#     # 'military_service',) 
#     # inlines=[EmployeeInline]

#     list_display = ['get_employee_name', 'get_employee_phone_number','get_employee_address',
#     'get_employee_city', 'get_employee_zip_code',  'get_medical_form']
#     #list_editable = ['get_employee_phone_number']
#     #list_filter = ['type', 'status', 'date_created', 'updated_at']
#     #search_fields = ['name', 'last_name', 'status']

#     def get_employee_name(self, obj):
        
#         return obj.employee.full_name
    
#     def get_medical_form(self, obj):
#         medicalForm = MedicalForm.objects.filter(employee = obj.employee)
#         print(medicalForm)
#         if not medicalForm.exists():
#             print("NONE")
#         return obj.employee.full_name
#     get_medical_form.short_description = 'name'

#     def get_employee_phone_number(self, obj):
#         return obj.employee.phone_number
#     get_employee_phone_number.short_description = 'phone number'

#     def get_employee_address(self, obj):
#         return obj.employee.address
#     get_employee_address.short_description = 'address'

#     def get_employee_city(self, obj):
#         return obj.employee.city
#     get_employee_city.short_description = 'city'

#     def get_employee_zip_code(self, obj):
#         return obj.employee.zip_code
#     get_employee_zip_code.short_description = 'zip code'

#     def get_employee_phone_number(self, obj):
#         return obj.employee.phone_number
#     get_employee_phone_number.short_description = 'phone number'

#     def get_employee_phone_number(self, obj):
#         return obj.employee.phone_number
#     get_employee_phone_number.short_description = 'phone number'

#     def get_employee_phone_number(self, obj):
#         return obj.employee.phone_number
#     get_employee_phone_number.short_description = 'phone number'

admin.site.register(Employee_head)
admin.site.register(Job)
admin.site.register(Department)
admin.site.register(Location)
admin.site.register(Document)



# admin.site.register(State, StateAdmin)
# admin.site.register(City, CityAdmin)
# admin.site.register(Location, LocationAdmin)
# admin.site.register(Department, DepartmentAdmin)
# admin.site.register(Job, JobAdmin)
#admin.site.register(Employee, EmployeeAdmin)
#admin.site.register(Application, ApplicationAdmin)
# admin.site.register(Emergency_contact, EmergencyContactAdmin)
# admin.site.register(Document, DocumentAdmin)
# admin.site.register(MedicalForm, MedicalFormAdmin)
# admin.site.register(Transaction, TransactionAdmin)
# admin.site.register(JobHistory, JobHistoryAdmin)

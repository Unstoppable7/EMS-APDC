from django.contrib import admin
from .models import State, City, Location, Department, Job, Employee, Application, Emergency_contact, Document, MedicalForm, Transaction, JobHistory

class StateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['name']
    search_fields = ['name']

class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'state']
    list_filter = ['name', 'state']
    search_fields = ['name']

class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'phone_number', 'zip_code', 'city']
    list_filter = ['name', 'address', 'phone_number', 'zip_code', 'city']
    search_fields = ['name']

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'location']
    list_filter = ['name', 'location']
    search_fields = ['name']

class JobAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'department']
    list_filter = ['name', 'department']
    search_fields = ['name']

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'last_name', 'mail', 'type', 'status', 'date_created', 'updated_at']
    list_filter = ['type', 'status', 'date_created', 'updated_at']
    search_fields = ['name', 'last_name', 'mail', 'status']

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'days_available_to_work', 'can_travel', 'can_work_nights', 'can_background_check', 'position_to_apply', 'experience', 'english_level', 'studies', 'military_service', 'file', 'employee']
    list_filter = ['days_available_to_work', 'can_travel', 'can_work_nights', 'can_background_check', 'position_to_apply', 'experience', 'english_level', 'studies', 'military_service']
    search_fields = ['employee__name', 'employee__last_name']

class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone_number', 'relationship', 'employee']
    list_filter = ['relationship']
    search_fields = ['employee__name', 'employee__last_name']

class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'number', 'date_of_expiration', 'file', 'employee']
    list_filter = ['type', 'date_of_expiration']
    search_fields = ['employee__name', 'employee__last_name']

class MedicalFormAdmin(admin.ModelAdmin):
    list_display = ['height', 'weight', 'allergic_to', 'diseases_suffered', 'received_workers_compensation', 'received_surgery_for_fracture']
    search_fields = ['name']

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['Reference', 'Start_date', 'End_date', 'Regular_hours', 'Regular_rate', 'Overtime_hours', 'Overtime_rate', 'Total_hours', 'Subtotal', 'Extra', 'Total_gross', 'Status', 'Payment_date', 'Withdrawn_date']
    search_fields = ['name']

class JobHistoryAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'end_date']
    search_fields = ['name']

admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Emergency_contact, EmergencyContactAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(MedicalForm, MedicalFormAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(JobHistory, JobHistoryAdmin)

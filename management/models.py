from django.db import models
from django.contrib import admin
import datetime

from django.db.models import Q

from django.utils.translation import gettext_lazy as _

from django.core.exceptions import ValidationError
import pdb

from phonenumber_field.modelfields import PhoneNumberField
#from address.models import AddressField

def current_time():
    return datetime.datetime.now()

# Create your models here.

class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name.capitalize()

class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='city_state')

    def __str__(self):
        return self.name.capitalize()

class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name='location')
    address = models.CharField(max_length=200,blank=True)
    phone_number = models.CharField(max_length=20,blank=True)
    zip_code = models.CharField(max_length=10,blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name.capitalize()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.
        dpt = Department.objects.create(name='Coordination',location=self)
        Job.objects.create(name='Coordinator',department=dpt)

class Department(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.name.capitalize()

class Job(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return ("%s - %s" % (self.name, self.department.location.name)).capitalize()
    
class Employee(models.Model): 
    TYPES_CHOICES = [
        ('Payroll', 'Payroll'),
        ('I9', 'I9'),
        ('Regular', 'Regular')
    ]
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Stand By', 'Stand By'),
        ('Do Not Hire', 'Do Not Hire'),
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Undefined', 'Undefined'),
    ]
    APPLICATION_STATUS_CHOICES = [
        ('FrontDesk', 'FrontDesk'),
        ('No Application', 'No Application'),
        ('Regular Application', 'Regular Application'),
        ('Southeast', 'Southeast'),
        ('Human Resources', 'Human Resources'),
        ('Undefined', 'Undefined'),
    ]

    QUICKBOOKS_STATUS_CHOICES = [
        ('Ready', 'Ready'),
        ('Not Hired', 'Not Hired'), #status default
        ('New Employee', 'New Employee'),
        ('Update Personal Information', 'Update Personal Information'),
        ('Update Address', 'Update Address'),
        ('Update to Inactive', 'Update to Inactive'),
        ('Update to Active', 'Update to Active'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    #address = AddressField()

    #phone_number = models.CharField(max_length=20, error_messages={'unique': _("This phone number is already in use."),})
    phone_number = PhoneNumberField()
    date_of_birth = models.DateField()
    email = models.EmailField(blank=True)
    #Payroll, etc
    type = models.CharField(max_length=10, choices=TYPES_CHOICES, default="Regular")
    zip_code = models.CharField(max_length=10)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="Undefined")
    application_status = models.CharField(max_length=20, choices=APPLICATION_STATUS_CHOICES, default="Undefined")
    quickbooks_status = models.CharField(max_length=30, choices=QUICKBOOKS_STATUS_CHOICES, default="Not Hired")
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=current_time)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.first_name

    @property
    @admin.display(
        ordering='last_name',
        description='Full name',
    )
    def full_name(self):
        return ("%s %s" % (self.first_name, self.last_name))

    class Meta:
        verbose_name = 'Company Employee'
        unique_together = (('phone_number', 'date_of_birth'),)
        
    def save(self, *args, **kwargs):
        #pdb.set_trace()
        #Empleado antes de ser guardado
        employee_old = Employee.objects.filter(pk=self.pk)
        employee_old_object =  employee_old.first()

        if(self.status != "Active"):
            for e in Employee_job.objects.filter(employee=self):
                e.delete()
        
        if employee_old_object != None:

            if employee_old_object.status == 'Stand By' and self.status != "Stand By":
                Employee_head.objects.filter(employee=employee_old_object).delete()
                #pdb.set_trace()

            #Si el empleado ya ha sido subido a Quickbooks
            if(employee_old_object.quickbooks_status == "Ready"):


                ##Cuando pasa de inactivo a activo se ejecutan estos dos if, sin embargo, funciona porque el ultimo es el que me interesa
                #Empleado a cambiado de status a Do Not Hire o Inactive
                if((employee_old_object.status != "Inactive" and employee_old_object.status != "Do Not Hire") and (self.status == "Do Not Hire" or self.status == "Inactive")):
                    #Cambiar en Quickbooks a inactivo
                    self.quickbooks_status = "Update to Inactive"
                    #pdb.set_trace()
                if (employee_old_object.status == "Inactive" or employee_old_object.status == "Do Not Hire") and (self.status != "Do Not Hire" and self.status != "Inactive"):
                    self.quickbooks_status = "Update to Active"

                #Empleado a cambiado de nombres, apellidos o numero de telefono
                if(employee_old_object.first_name != self.first_name or employee_old_object.last_name != self.last_name or employee_old_object.phone_number != self.phone_number or employee_old_object.date_of_birth != self.date_of_birth):
                    self.quickbooks_status = "Update Personal Information"

                #Empleado a cambiado de direccion
                if employee_old_object.address != self.address:
                    self.quickbooks_status = "Update Address"
        
        super().save(*args, **kwargs)
        
class EmployeeInterview(Employee): 
    class Meta:
        proxy = True
        verbose_name = 'Interview'
        
class MyEmployeeSection(Employee): 
    class Meta:
        proxy = True
        verbose_name = 'My employee'
        ordering = ['-status']

class Recruiting(Employee): 
    class Meta:
        proxy = True
        verbose_name = 'Recruiting'

class EmployeeManagement(Employee): 
    class Meta:
        proxy = True
        verbose_name = 'Employee Management'
        verbose_name_plural = 'Employee Management'
        ordering = ['date_created']

class AccountingStatus(Employee): 
    class Meta:
        proxy = True
        verbose_name = 'Accounting Status'
        verbose_name_plural = 'Accounting Status'
        ordering = ['updated_at']

class Employee_head(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employeeWithHead')
    head = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='head')

    def __str__(self):
        return f'{self.employee.full_name} - {self.head.full_name}'
    
    # class Meta:
    #     verbose_name = 'Coordinator Employee'

    def __eq__(self, other):
        return self.employee == other.employee and self.head == other.head

class Employee_job(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_job_employee')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job')

    #Sobrescribimos el metodo save
    def save(self, *args, **kwargs):

        #Buscamos en el objeto antes de ser editado
        employee_job_old = Employee_job.objects.filter(pk=self.pk)
         
        #Buscamos en el objeto antes de ser editado si tiene un trabajo de coordinator
        employee_job_coordinator_old = employee_job_old.filter(job__name="Coordinator")
        
        #Variable que usaremos para definir si antes de ejecutar este save tenia un trabajo de coordinator
        was_coordinator = False

        #Si el objeto antes de ser editado si tiene un trabajo de coordinator y el trabajo que se le esta asignando es diferente a coordinator, hacemos true nuestra bandera
        if employee_job_coordinator_old.exists() and self.job.name != 'Coordinator':
            was_coordinator = True

        #Metodo padre que guarda el objeto en la db
        super().save(*args, **kwargs)  # Call the "real" save() method.
        
        # self.employee.status = "Active"
        # self.employee.save(update_fields=['status'])
        newQuickbooksStatus = self.employee.quickbooks_status

        if self.employee.quickbooks_status == "Not Hired":
            newQuickbooksStatus = "New Employee"
        
        if self.employee.status == "Inactive" or self.employee.status == "Do Not Hire":
            newQuickbooksStatus = "Update to Active"

        #Cambio el status del empleado a Active
        ###De esta manera solo se me ejecuta una vez el metodo Save()
        Employee.objects.filter(id=self.employee.id).update(status="Active",quickbooks_status=newQuickbooksStatus)
        
        #pdb.set_trace()
        #Si el cambio del objeto fue que su trabajo ahora sea coordinator o si venia de ser coordinator y ahora no lo es
        if self.job.name == 'Coordinator' or was_coordinator:
            
            #Eliminamos todos las referencias de este objeto como coordinator
            Employee_head.objects.filter(head=self.employee).delete()

            #Lista donde guardaremos las nuevas referencias de este objeto como coordinator
            employee_heads_to_create = []

            #Recorremos todos los trabajos que sean de coordinator de este empleado
            for employee_job_employee in Employee_job.objects.filter(employee=self.employee).filter(job__name="Coordinator"):
                
                #Guardamos la locacion de cada trabajo
                location = employee_job_employee.job.department.location

                #Recorremos cada empleado que tiene un trabajo con esa locacion exceptuando los trabajos de coordinator
                for employee_job_employee in Employee_job.objects.filter(job__department__location=location).exclude(job__name='Coordinator'):
                    
                    #Agregamos la referencia del empleado con el coordinator a la lista
                    employee_heads_to_create.append(Employee_head(employee=employee_job_employee.employee, head=self.employee))
            try:
                #Intentamos crear en la db todos los objetos de la lista
                Employee_head.objects.bulk_create(employee_heads_to_create)
            except:
                pass

        #Eliminamos todas las referencias de este objeto como empleado de un coordinator
        Employee_head.objects.filter(employee=self.employee).delete()
        
        #Lista donde guardaremos las nuevas referencias
        employee_heads_to_create = []

        #Recorremos cada trabajo de este empleado exceptuando los trabajos de coordinador
        for employee_job_employee in Employee_job.objects.filter(employee=self.employee).exclude(job__name='Coordinator'):
            
            #Guardamos la locacion de cada trabajo
            location = employee_job_employee.job.department.location

            #Recorremos todos los coordinadores que tienen esa locacion
            for employee_job_coordinator in Employee_job.objects.filter(job__department__location=location).filter(job__name='Coordinator'):
                
                #Evitamos duplicados, si no ha sido agregado la referencia a la lista procedemos
                if not Employee_head(employee=self.employee, head=employee_job_coordinator.employee) in employee_heads_to_create:

                    #Agregamos la referencia del empleado con el coordinator a la lista
                    employee_heads_to_create.append(Employee_head(employee=self.employee, head=employee_job_coordinator.employee))
        try:
            #Intentamos crear en la db todos los objetos de la lista
            Employee_head.objects.bulk_create(employee_heads_to_create)
        except:
            pass

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        
        if self.job.name == 'Coordinator':

            Employee_head.objects.filter(head=self.employee).delete()

            employee_heads_to_create = []
            
            for employee_job_employee in Employee_job.objects.filter(employee=self.employee).filter(job__name="Coordinator"):

                location = employee_job_employee.job.department.location

                for employee_job_employee in Employee_job.objects.filter(job__department__location=location).exclude(job__name='Coordinator'):
                
                    employee_heads_to_create.append(Employee_head(employee=employee_job_employee.employee, head=self.employee))
            try:
                Employee_head.objects.bulk_create(employee_heads_to_create)
            except:
                pass

        Employee_head.objects.filter(employee=self.employee).delete()

        employee_heads_to_create = []

        for employee_job_employee in Employee_job.objects.filter(employee=self.employee).exclude(job__name='Coordinator'):
            
            location = employee_job_employee.job.department.location

            for employee_job_coordinator in Employee_job.objects.filter(job__department__location=location).filter(job__name='Coordinator'):
                
                if not Employee_head(employee=self.employee, head=employee_job_coordinator.employee) in employee_heads_to_create:

                    employee_heads_to_create.append(Employee_head(employee=self.employee, head=employee_job_coordinator.employee))
        try:
            Employee_head.objects.bulk_create(employee_heads_to_create)
        except:
            pass

    def __str__(self):
        return f'{self.employee.full_name} - {self.job}'
    class Meta:
        unique_together = (('employee', 'job'),)
        verbose_name = "Employee Job"


# @receiver(pre_save, sender=Employee_job)
# def pre_save_employee_job(sender, instance, **kwargs):
#     print('\n\n')
#     print(instance.employee)
#     print('\n\n')

    # #jobs = Employee_job.objects.filter(employee=instance)
    # jobs = Employee_job.objects.get_or_create(employee=instance, defaults={'employee': instance, 'head': head})
    # print('\n\n')
    # print(jobs)
    # print('\n\n')

    # job_department_location = instance.job.department.location

    # try:

    #     head = Employee.objects.select_related("job__department__location").filter(job__department__location__id=job_department_location.id, job__name="Coordinator").first()

    #     relation, created = Employee_head.objects.get_or_create(employee=instance, defaults={'employee': instance, 'head': head})

    #     if not created:
    #         relation.head = head
    #         relation.save()
    # except:
    #     print("ENTRA EN EXCEPT DE pre_save_employee_head")
    #     pass
      
class Application(models.Model):
    DAYS_AVAILABLE_TO_WORK_CHOICES = [
        ('Monday to Friday', _('Monday to Friday')),
        ('Monday to Saturday', _('Monday to Saturday')),
        ('Monday to Sunday', _('Monday to Sunday')),
    ]
    POSITION_TO_APPLY_CHOICES = [
        ('Manager', 'Manager'),
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
        ('All the positions', _('All the positions')),
        ('Other', _('Other')),
    ]
    ENGLISH_LEVEL_CHOICES = [
        ('None', _('None')),
        ('Basic', _('Basic')),
        ('Intermediate', _('Intermediate')),
        ('Advanced', _('Advanced')),
    ]
    STUDIES_LEVEL_CHOICES = [
        ('None', _('None')),
        ('High school', 'High school'),
        ('University', 'University'),
    ]
    CHOICES_BOOLEAN_YES_NO = (
        (True, _('Yes')),
        (False, _('No'))
    )
    days_available_to_work = models.CharField(max_length=20, choices=DAYS_AVAILABLE_TO_WORK_CHOICES)
    # can_travel = models.BooleanField()
    #HERE
    can_travel = models.BooleanField(choices=CHOICES_BOOLEAN_YES_NO)
    #can_travel = models.TypedChoiceField(label=_('If Hired, Are You Willing To Test For Controlled Substances?'),coerce=lambda x: x =='True', choices=((False, 'No'), (True, 'Yes')))
    # can_work_nights = models.BooleanField()
    can_work_nights = models.BooleanField(choices=CHOICES_BOOLEAN_YES_NO)
    # can_background_check = models.BooleanField()
    can_background_check = models.BooleanField(choices=CHOICES_BOOLEAN_YES_NO)
    position_to_apply = models.CharField(max_length=25, choices=POSITION_TO_APPLY_CHOICES)
    experience = models.CharField(max_length=500)
    english_level = models.CharField(max_length=12, choices=ENGLISH_LEVEL_CHOICES)
    studies = models.CharField(max_length=12, choices=STUDIES_LEVEL_CHOICES)
    specialty_of_studies = models.CharField(max_length=50, blank=True)
    # military_service = models.BooleanField()
    military_service = models.BooleanField(choices=CHOICES_BOOLEAN_YES_NO)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='application_employee')

    def __str__(self):
        return self.employee.full_name

class Emergency_contact(models.Model):
    name = models.CharField(max_length=50)
    phone_number = PhoneNumberField()
    relationship = models.CharField(max_length=20)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Emergency Contact"


class Document(models.Model):
    TYPE_CHOICES = [
        ('Application', 'Application'),
        ('Southeast', 'Southeast'),
        ('Form', 'Form'),
        ('Passport', 'Passport'),
        ('Driver license', 'Driver license'),
        ('ID card', 'ID card'),

    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_of_expiration = models.DateField(blank=True, null=True,)
    file = models.FileField(upload_to='employee_documents/')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.type

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.type == "Application":
            for e in Employee.objects.filter(id=self.employee):
                e.application_status = 'Regular Application'
                e.save()
        elif self.type == "Southeast":    
            for e in Employee.objects.filter(id=self.employee.id):
                e.application_status = 'Southeast'
                e.save()

    def delete(self, *args, **kwargs):
        if self.type == "Application":
            for e in Employee.objects.filter(id=self.employee.id):
                e.application_status = 'Undefined'
                e.save()
        elif self.type == "Southeast":    
            for e in Employee.objects.filter(id=self.employee.id):
                e.application_status = 'Undefined'
                e.save()
        super().delete(*args, **kwargs)


class MedicalForm(models.Model):
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    allergic_to = models.CharField(max_length=100)
    diseases_suffered = models.CharField(max_length=100)
    received_workers_compensation = models.CharField(max_length=100)
    received_surgery_for_fracture = models.CharField(max_length=100)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.employee.first_name

class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)

class FrequentPaymentMethod(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    reference = models.CharField(max_length=100)

class Transaction(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    Reference = models.CharField(max_length=50, blank=True)
    Start_date = models.DateField()
    End_date = models.DateField()
    Regular_hours = models.DecimalField(max_digits=5, decimal_places=2)
    Regular_rate = models.DecimalField(max_digits=5, decimal_places=2)
    Overtime_hours = models.DecimalField(max_digits=5, decimal_places=2)
    Overtime_rate = models.DecimalField(max_digits=5, decimal_places=2)
    Total_hours = models.DecimalField(max_digits=5, decimal_places=2)
    Subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    Extra = models.DecimalField(max_digits=10, decimal_places=2)
    Total_gross = models.DecimalField(max_digits=10, decimal_places=2)
    Status = models.CharField(max_length=20)
    Payment_date = models.DateField(null=True, blank=True)
    Withdrawn_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.first_name

class JobHistory(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name

# @receiver(post_save, sender=Employee)
# def create_employee_head(sender, instance, created, **kwargs):
#     if created:
#         try:
#             location = instance.job.department.location
#             head = Employee.objects.select_related("job__department__location").filter(job__department__location__id=location.id, job__name="Coordinator").values()
#             Employee_head.objects.create(employee=instance, head=head)
#         except:
#             pass
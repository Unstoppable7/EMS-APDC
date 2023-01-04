from django.db import models
import datetime

def current_time():
    return datetime.datetime.now()

# Create your models here.

class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200,blank=True)
    phone_number = models.CharField(max_length=20,blank=True)
    zip_code = models.CharField(max_length=10,blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

def get_default_none_job():
    noneState = State.objects.get_or_create(name="None")[0]
    noneCity = City.objects.get_or_create(name="None", state=noneState)[0]
    noneLocation = Location.objects.get_or_create(name="None", city=noneCity)[0]
    noneDepartment = Department.objects.get_or_create(name="None", location=noneLocation)[0]
    return Job.objects.get_or_create(name="None", department=noneDepartment)[0]

class Job(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Employee(models.Model): 
    TYPES_CHOICES = [
        ('Payroll', 'Payroll'),
        ('I9', 'I9'),
        ('Regular', 'Regular')
    ]
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Interview', 'Interview'),
    ]
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    mail = models.EmailField(blank=True)
    #Payroll, etc
    type = models.CharField(max_length=10, choices=TYPES_CHOICES, default="Regular")
    zip_code = models.CharField(max_length=10)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Interview")
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, default= get_default_none_job, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=current_time)
    updated_at = models.DateTimeField(default=current_time)
    
    def __str__(self):
        return self.name

    @property
    def full_name(self):
        return f'{self.name} {self.last_name}'
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        super(Employee, self).save(*args, **kwargs)

class Application(models.Model):
    DAYS_AVAILABLE_TO_WORK_CHOICES = [
        ('Mon-Fri', 'Monday to Friday'),
        ('Mon-Sat', 'Monday to Saturday'),
        ('Mon-Sun', 'Monday to Sunday')
    ]
    POSITION_TO_APPLY_CHOICES = [
        ('Manager', 'Manager'),
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
        ('All the positions', 'All the positions'),
        ('Other', 'Other'),
    ]
    EXPERIENCE_CHOICES = [
        ('Manager', 'Manager'),
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
        ('Other', 'Other'),
    ]
    ENGLISH_LEVEL_CHOICES = [
        ('None', 'None'),
        ('Basic', 'Basic'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Fluent', 'Fluent')
    ]
    days_available_to_work = models.CharField(max_length=8, choices=DAYS_AVAILABLE_TO_WORK_CHOICES)
    can_travel = models.BooleanField()
    can_work_nights = models.BooleanField()
    can_background_check = models.BooleanField()
    position_to_apply = models.CharField(max_length=17, choices=POSITION_TO_APPLY_CHOICES)
    experience = models.CharField(max_length=15, choices=EXPERIENCE_CHOICES)
    english_level = models.CharField(max_length=12, choices=ENGLISH_LEVEL_CHOICES)
    studies = models.BooleanField()
    military_service = models.BooleanField()
    file = models.FileField(upload_to='applications/')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Emergency_contact(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    relationship = models.CharField(max_length=20)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Document(models.Model):
    TYPE_CHOICES = [
        ('Passport', 'Passport'),
        ('Driver license', 'Driver license'),
        ('ID card', 'ID card'),
        ('Social security card', 'Social security card'),
        ('Work permit', 'Work permit')
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    number = models.CharField(max_length=20)
    date_of_expiration = models.DateField()
    file = models.FileField(upload_to='employee_documents/')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class MedicalForm(models.Model):
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    allergic_to = models.CharField(max_length=50, blank=True)
    diseases_suffered = models.CharField(max_length=50, blank=True)
    received_workers_compensation = models.BooleanField(default=False)
    received_surgery_for_fracture = models.BooleanField(default=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

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
        return self.name

class JobHistory(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

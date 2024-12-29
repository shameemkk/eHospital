from django.db import models
from doctor.models import Doctor

# Create your models here.

class LoginType(models.Model):
    TYPE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    ]
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="type")
    type = models.CharField(max_length=100,choices=TYPE_CHOICES)

class Patient(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="patient")
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"patient--{self.name}"

class Slot(models.Model):
    slot_name = models.CharField(max_length=10)
    time = models.TimeField()

    def __str__(self):
        return self.slot_name

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed')
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    prescription = models.ForeignKey('Prescription', on_delete=models.CASCADE, blank=True, null=True)
    appointment_date = models.DateTimeField()
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.patient.name


class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    medications = models.TextField()
    allergies = models.TextField()
    treatment_history = models.TextField()
    date_recorded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient.name
    

class Billing(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid')
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    billing_statement = models.TextField()
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES)
    insurance_info = models.TextField(blank=True, null=True)
    date_billed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient.name
    

class HealthEducationResource(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category= models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    medication = models.TextField()
    dosage = models.TextField()
    instructions = models.TextField()
    duration = models.CharField(max_length=50)
    date_prescribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient.name

from django.db import models

# Create your models here.

class Specialty(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='specialties/')  

    def __str__(self):
        return self.name
    

class Doctor(models.Model):
    user= models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="doctor")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='doctors/')
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE) 
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    license_number = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.specialty.name}"

  
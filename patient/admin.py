from django.contrib import admin
from .models import Patient,Appointment,Slot, MedicalHistory, Billing, HealthEducationResource, LoginType
# Register your models here.


admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Slot)
admin.site.register(MedicalHistory)
admin.site.register(Billing)
admin.site.register(HealthEducationResource)
admin.site.register(LoginType)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from doctor.models import Specialty, Doctor
from patient.models import Patient, Appointment, MedicalHistory, Slot, Billing, Prescription
import json
from django.utils import timezone

def index(request):
    return render(request, 'index.html')

@login_required
def doctor_dashboard(request):
    # Get the logged-in doctor
    user = request.user
    doctor = Doctor.objects.get(user=user)

    # Get the count of patients
    patients_count = Patient.objects.count()

    # Get today's date
    current_date = timezone.now().date()

    # Get upcoming appointments for the doctor
    upcoming_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date__gte=current_date
    ).order_by('appointment_date')

    # Get the count of upcoming appointments
    upcoming_appointments_count = upcoming_appointments.count()

    # Prepare context for rendering the template
    context = {
        'patients_count': patients_count,
        'upcoming_appointments_count': upcoming_appointments_count,
        'appointments': upcoming_appointments,
        'current_year': timezone.now().year,  # For footer copyright
    }

    # Render the doctor dashboard template
    return render(request, 'doctor/doctor_dashboard.html', context)

def specialty_list(request):
    specialties = Specialty.objects.all()
    context = {
        'specialties': specialties
    }
    return render(request, 'doctor/specialty_list.html', context)

def doctor_list(request, specialty_id: int):
    specialty = Specialty.objects.get(id=specialty_id)
    doctors = Doctor.objects.filter(specialty=specialty)
    context = {
        'doctors': doctors,
        'specialty': specialty
    }
    return render(request, 'doctor/doctor-list.html', context)

@login_required
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'doctor/patient_list.html', {'patients': patients})

@login_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    medical_history = MedicalHistory.objects.filter(patient=patient).order_by('-date_recorded')
    appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')
    billings = Billing.objects.filter(patient=patient).order_by('-date_billed')
    prescriptions = Prescription.objects.filter(patient=patient).order_by('-date_prescribed')
    
    context = {
        'patient': patient,
        'medical_history': medical_history,
        'appointments': appointments,
        'billings': billings,
        'prescriptions': prescriptions,
    }
    return render(request, 'doctor/patient_detail.html', context)

@login_required
def appointment_schedule_list(request):
    user = request.user
    doctor=Doctor.objects.get(user=user)
    current_date = timezone.now().date()
    appointments=Appointment.objects.filter(
        doctor=doctor,
        appointment_date__gte=current_date
    ).order_by('slot__slot_name')
    context = {
        'appointments': appointments
    }

    return render(request, 'doctor/appointment_schedule.html', context)

@login_required
def appointment_status_change(request, appointment_id):
    status=request.POST.get('status')
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = status
    appointment.save()
    return redirect('appointment_schedule_list')

@login_required
def e_prescribe(request, patient_id, appointment_id):
    if request.method == 'POST':
        patient = get_object_or_404(Patient, id=patient_id)
        doctor = Doctor.objects.get(user=request.user)
        appointment = get_object_or_404(Appointment, id=appointment_id)
        appointment.status = 'completed'
        prescription = Prescription.objects.create(
            patient=patient,
            doctor=doctor,
            medication=request.POST['medication'],
            dosage=request.POST['dosage'],
            instructions=request.POST['instructions'],
            duration=request.POST['duration']
        )
        appointment.prescription = prescription
        appointment.save()
        
        return redirect('appointment_schedule_list')


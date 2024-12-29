from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Patient,Appointment,Slot, LoginType, MedicalHistory, Billing, HealthEducationResource
from doctor.models import Doctor
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.utils import timezone



# Create your views here.
def patient_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard_route')
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'patient/login.html')

def patient_registration(request):
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        gender = request.POST['gender']
        phone_number = request.POST['phone_number']
        address = request.POST['address']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['cpassword']
        if Patient.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('patient_registration')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('patient_registration')
        else:
            user = User.objects.create_user(username=email, password=password)
            patient = Patient(name=name, age=age, gender=gender, 
                                       phone_number=phone_number, address=address, 
                                       email=email, user=user)
            patient.save()
            logintype=LoginType(user=user,type='patient')
            logintype.save()
            messages.success(request, 'Registration successful! You can now login.')
            return redirect('patient_login')

    return render(request, 'patient/register.html')
            
@login_required
def patient_dashboard(request):
    patient = Patient.objects.get(user=request.user)
    next_appointment = Appointment.objects.filter(
        patient=patient, 
        status='scheduled'
    ).order_by('appointment_date').first()
    last_medical_history = MedicalHistory.objects.filter(
        patient=patient
    ).order_by('-date_recorded').first()

    current_balance = Billing.objects.filter(
        patient=patient, 
        payment_status='unpaid'
    ) or 0
    if current_balance:
        current_balance = sum([bill.amount_due for bill in current_balance])

    education_resource=HealthEducationResource.objects.all().order_by('-created_at')[:3]

    bills=Billing.objects.filter(patient=patient)

    context = {
        'bills': bills,
        'patient': patient,
        'next_appointment': next_appointment,
        'last_medical_history': last_medical_history,
        'education_resource': education_resource,
        'current_balance': current_balance,
    }

    return render(request, 'patient/patient_dashboard.html', context)

@login_required
def view_full_history(request):
    patient = Patient.objects.get(user=request.user)
    medical_history = MedicalHistory.objects.filter(patient=patient).order_by('-date_recorded')

    context = {
        'patient': patient,
        'medical_history': medical_history,
    }
    return render(request, 'patient/view_full_history.html', context)

@login_required
def health_education_resources(request):
    patient = Patient.objects.get(user=request.user)
    resources = HealthEducationResource.objects.all().order_by('-created_at')

    context = {
        'patient': patient,
        'resources': resources,
    }

    return render(request, 'patient/health_education_resources.html', context)

@login_required
def health_education_resource_detail(request, resource_id):
    patient = Patient.objects.get(user=request.user)
    resource = HealthEducationResource.objects.get(id=resource_id)
    context = {
        'patient': patient,
        'resource': resource,
    }

    return render(request, 'patient/health_education_resource_detail.html', context)


@login_required
def dashboard_route(request):
    user = request.user
    login_type = LoginType.objects.get(user=user)
    if login_type.type == 'patient':
        return redirect('patient_dashboard')
    elif login_type.type == 'doctor':
        return redirect('doctor_dashboard')

def logout_user(request):
    logout(request)
    return redirect('index')

def profile_edit(request):
    if request.method == 'POST':
        user = request.user
        patient = Patient.objects.get(user=user)
        name = request.POST['name']
        age = request.POST['age']
        gender = request.POST['gender']
        phone_number = request.POST['phone_number']
        patient.name = name
        patient.age = age
        patient.gender=gender
        patient.phone_number=phone_number
        patient.save()
        return redirect('patient_dashboard')


def appointment_date(request,doctor_id):
    doctor=Doctor.objects.get(id=doctor_id)
    if request.method == 'POST':
        date = request.POST['date']
        appointment=Appointment.objects.filter(doctor=doctor,appointment_date=date)
        if not appointment:
            slots=Slot.objects.all()
            data={
                'slots':slots,
                'doctor':doctor,
                'date':date
                }
            return render(request,'patient/appointment_submit.html',data)
        else:
            scheduled_appointments=[app.slot for app in appointment] 
            available_slots=[slot for slot in Slot.objects.all() if slot not in scheduled_appointments]
            data={
                'slots':available_slots,
                'doctor':doctor,
                'date':date
                }
            return render(request,'patient/appointment_submit.html',data)
    context={
        'doctor':doctor,
    }
    return render(request, 'patient/appointment_date.html',context)

def appoinment_submit(request,doctor_id,date):
    if request.method == 'POST':
        print(request.POST)
        date = date
        slot_id = request.POST.get('slot')
        slot=Slot.objects.get(id=slot_id)
        doctor=Doctor.objects.get(id=doctor_id)
        patient=Patient.objects.get(user=request.user)
        appointmet_slot=Appointment.objects.filter(appointment_date=date, slot=slot, doctor=doctor).exists()
        if appointmet_slot:
            messages.error(request, 'Appointment already scheduled')
            return redirect('appointment_date',doctor_id=doctor_id)
        else:
            appointmet= Appointment(
                patient=patient,
                appointment_date=date,
                slot=slot,
                doctor=doctor,
                status="scheduled"
                )
            appointmet.save()
            return redirect('patient_dashboard')
        

def cancel_appointment(request,appointment_id):
    appointment=Appointment.objects.get(id=appointment_id)
    appointment.delete()
    return redirect('patient_dashboard')

@login_required
def patient_appointment_list(request):
    patient = Patient.objects.get(user=request.user)
    current_date = timezone.now().date()
    
    upcoming_appointments = Appointment.objects.filter(
        patient=patient,
        appointment_date__gte=current_date,
        status='scheduled'
    ).order_by('appointment_date')
    
    past_appointments = Appointment.objects.filter(
        patient=patient,
    ).exclude(status='scheduled').order_by('-appointment_date')

    context = {
        'patient': patient,
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
    }

    return render(request, 'patient/patient_appointment_list.html', context)

@login_required
def reschedule_appointment(request,appointment_id):
    appointment=Appointment.objects.get(id=appointment_id)
    doctor=appointment.doctor
    date= appointment.appointment_date.date()
    if request.method == 'POST':
        slot_id = request.POST.get('slot')
        slot=Slot.objects.get(id=slot_id)
        appointment.slot=slot
        appointment.save()
        return redirect('patient_dashboard')
    appointments=Appointment.objects.filter(doctor=doctor,appointment_date=date)
    scheduled_appointments=[app.slot for app in appointments] 
    available_slots=[slot for slot in Slot.objects.all() if slot not in scheduled_appointments]
    data={
        'appointment':appointment,
        'slots':available_slots,
        'doctor':doctor,
        'date':date
        }
    return render(request,'patient/appointment_reschedule.html',data)
    
        

def medical_history(request):
    return render(request, 'patient/medical_history.html')


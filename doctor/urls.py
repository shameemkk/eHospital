
from django.urls import path
from . import views

urlpatterns = [
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('specialties/', views.specialty_list, name='specialty-list'),
    path('doctors/<int:specialty_id>/', views.doctor_list, name='doctor-list'),
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('appointment_schedule_list/', views.appointment_schedule_list, name='appointment_schedule_list'),
    path('appointment_status_change/<int:appointment_id>/', views.appointment_status_change, name='appointment_status_change'),
    path('doctor/e_prescribe/<int:patient_id>/<int:appointment_id>/', views.e_prescribe, name='e_prescribe'),

]


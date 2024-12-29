from django.urls import path
from . import views

urlpatterns = [
    path('patient-registration/', views.patient_registration, name='patient_registration'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('view_full_history/', views.view_full_history, name='view_full_history'),
    path('health_education_resources/', views.health_education_resources, name='health_education_resources'),
    path('health-education/<int:resource_id>/', views.health_education_resource_detail, name='health_education_resource_detail'),
    path('logout/', views.logout_user, name='logout_user'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('dashboard_route/', views.dashboard_route, name='dashboard_route'),
    path('patient-login/', views.patient_login, name='patient_login'),
    path('appointment_date/<doctor_id>',views.appointment_date, name='appointment_date'),
    path('patient/appoinment_submit/<int:doctor_id>/<str:date>/',views.appoinment_submit, name='appoinment_submit'),
    path('patient/cancel_appointment/<int:appointment_id>/',views.cancel_appointment, name='cancel_appointment'),
    path('patient/patient_appointment_list/',views.patient_appointment_list, name='patient_appointment_list'),
    path('patient/reschedule_appointment/<int:appointment_id>/',views.reschedule_appointment, name='reschedule_appointment'),

]
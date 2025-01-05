from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.SimpleRouter()
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'department', DepartmentViewSet, basename='departments')
router.register(r'appointment', AppointmentViewSet, basename='appointment')
router.register(r'prescriptions', PrescriptionsViewSet, basename='prescriptions')
router.register(r'billing', BillingViewSet, basename='billing')
router.register(r'wards', WardViewSet, basename='ward')
router.register(r'feedback', FeedbackViewSet, basename='feedback')





urlpatterns =[
    path('', include(router.urls)),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('create/profile', ProfileCreateApiView.as_view(), name = 'create_profile'),
    path('speciality/', SpecialityApiView.as_view(), name = 'speciality'),
    path('doctors/', DoctorListApiView.as_view(), name = 'doctor_list'),
    path('doctors/<int:pk>/', DoctorDetailApiView.as_view(), name = 'doctor_detail'),
    path('doctors/create/', DoctorCreateApiView.as_view(), name = 'doctor_create'),
    path('patients/', PatientListApiView.as_view(), name = 'patient_list'),
    path('patients/<int:pk>/', PatientDetailApiView.as_view(), name = 'patient_detail'),
    path('appointments/create/', AppointmentCreateApiView.as_view(), name = 'appointment'),
    path('medical_record/', MedicalRecordApiView.as_view(), name = 'medical_record')
]
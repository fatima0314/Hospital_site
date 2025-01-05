from django.contrib.auth import authenticate
from django.db.migrations.serializer import TypeSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *


class ProfileRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'email', 'password' ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
            user = Profile.objects.create_user(**validated_data)
            return user


    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")


    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'role', 'phone_number', 'profile_picture', 'address', 'date_of_birth']



class PatientSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id']



class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = ['speciality_name']



class DepartmentSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name', 'location']



class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id','name', 'head_id', 'location']



class AppointmentSimpleSerializer(serializers.ModelSerializer):
    date_time = serializers.DateTimeField(format='%d-%m-%Y  %H:%M')
    class Meta:
        model = Appointment
        fields = ['doctor_id', 'date_time', 'status', 'notes']



class AppointmentSerializer(serializers.ModelSerializer):
    date_time = serializers.DateTimeField(format='%d-%m-%Y  %H:%M')
    class Meta:
        model = Appointment
        fields = ['patient_id', 'doctor_id', 'date_time', 'status']



class PrescriptionsSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescriptions
        fields = ['medication', 'dosage']



class PrescriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescriptions
        fields = ['medical_record', 'medication', 'dosage']



class MedicalRecordSerializer(serializers.ModelSerializer):
    prescribed_medication = PrescriptionsSimpleSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(format='%d-%m-%Y  %H:%M')
    class Meta:
        model = MedicalRecord
        fields = ['patient_id','doctor_id', 'diagnosis', 'treatment', 'prescribed_medication', 'created_at']



class MedicalRecordSimpleSerializer(serializers.ModelSerializer):
    prescribed_medication = PrescriptionsSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(format='%d-%m-%Y  %H:%M')
    class Meta:
        model = MedicalRecord
        fields = ['doctor_id', 'diagnosis', 'treatment', 'prescribed_medication', 'created_at']



class BillingSimpleSerializer(serializers.ModelSerializer):
    issued_date = serializers.DateTimeField(format='%d-%m-%Y  %H:%M')
    class Meta:
        model = Billing
        fields = ['total_amount', 'paid', 'issued_date']



class BillingSerializer(serializers.ModelSerializer):
    issued_date = serializers.DateTimeField(format='%d-%m-%Y  %H:%M')
    class Meta:
        model = Billing
        fields = ['patient', 'total_amount', 'paid', 'issued_date']



class WardSerializer(serializers.ModelSerializer):
    free_seats = serializers.SerializerMethodField()
    class Meta:
        model = Ward
        fields = ['id', 'name', 'ward_types', 'capacity', 'current_occupancy', 'free_seats']


    def get_free_seats(self, obj):
         return obj.get_free_seats()



class FeedbackSimpleSerializer(serializers.ModelSerializer):
    patient = PatientSimpleSerializer()
    class Meta:
        model = Feedback
        fields = ['patient', 'rating', 'comment']



class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['patient', 'doctor', 'rating', 'comment']



class PatientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'user_id', 'emergency_contact', 'blood_type', 'medical_history', 'allergies']



class PatientDetailSerializer(serializers.ModelSerializer):
    medical_record = MedicalRecordSimpleSerializer(many=True, read_only=True)
    billing = BillingSimpleSerializer(many=True, read_only=True)
    patient_appointment = AppointmentSimpleSerializer(many=True, read_only=True)
    class Meta:
        model = Patient
        fields = [ 'id', 'user_id', 'emergency_contact', 'blood_type', 'medical_history', 'allergies','patient_appointment', 'medical_record', 'billing' ]



class DoctorListSerializer(serializers.ModelSerializer):
    specialty = SpecialitySerializer()
    department = DepartmentSimpleSerializer(many=True, read_only=True)
    shift_start = serializers.DateTimeField(format='%H:%M')
    shift_end =  serializers.DateTimeField(format='%H:%M')
    class Meta:
        model = Doctor
        fields = ['id', 'user_id', 'specialty','shift_start', 'shift_end', 'working_days','price', 'department']



class DoctorDetailSerializer(serializers.ModelSerializer):
    department = DepartmentSimpleSerializer(many=True, read_only=True)
    specialty = SpecialitySerializer()
    shift_start = serializers.DateTimeField(format='%H:%M')
    shift_end = serializers.DateTimeField(format='%H:%M')
    avg_rating = serializers.SerializerMethodField()
    review = FeedbackSimpleSerializer(many=True, read_only=True)
    class Meta:
        model = Doctor
        fields = ['id', 'user_id', 'specialty', 'qualification', 'shift_start', 'shift_end', 'working_days', 'experience_years', 'price', 'department', 'avg_rating', 'review']

    def get_avg_rating(self, obj):
         return obj.get_avg_rating()



class DoctorCreateSerializer(serializers.ModelSerializer):
    shift_start = serializers.DateTimeField(format='%H:%M')
    shift_end = serializers.DateTimeField(format='%H:%M')
    class Meta:
        model = Doctor
        fields = ['user_id','specialty', 'qualification', 'shift_start', 'shift_end', 'working_days', 'experience_years', 'price']
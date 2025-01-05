from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField



class Profile(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient')
    )
    role = models.CharField(choices=ROLE_CHOICES, default='patient', max_length=10)
    phone_number = PhoneNumberField(region='KG', null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    address = models.CharField(max_length=50)
    date_of_birth = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}-{self.last_name}'



class Speciality(models.Model):
    speciality_name = models.CharField(max_length=50)

    def __str__(self):
        return self.speciality_name



class Doctor(models.Model):
    user_id = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='doctors')
    specialty = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=100)
    shift_start = models.DateTimeField()
    shift_end = models.DateTimeField()
    DAYS_CHOICES = (
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    )
    working_days = MultiSelectField(choices=DAYS_CHOICES, null=True, blank=True)
    experience_years = models.PositiveSmallIntegerField(default=0)
    price = models.PositiveSmallIntegerField(default=0)


    def get_avg_rating(self):
        ratings = self.review.all()
        if ratings.exists():
            return round(sum(i.rating for i in ratings) / ratings.count(), 1)
        return 0



class Patient(models.Model):
    user_id = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='patients')
    emergency_contact = PhoneNumberField(region='KG', null=True, blank=True)
    blood_type = models.CharField(max_length=15)
    allergies = models.CharField(null=True,blank=True, max_length=100)
    medical_history = models.TextField(null=True, blank=True)



class Department(models.Model):
    name = models.CharField(max_length=50)
    head_id = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='department')
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Appointment(models.Model):
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_appointment')
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_appointment')
    date_time = models.DateTimeField()
    STATUS_APPOINTMENT = (
        ('запланировано', 'запланировано'),
        ('завершено', 'завершено'),
        ('отменено', 'отменено')
    )
    status = models.CharField(choices=STATUS_APPOINTMENT, max_length=18)
    notes = models.TextField()

    def __str__(self):
        return f'{self.doctor_id}-{self.patient_id}'



class MedicalRecord(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_record', default=0)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.patient_id}-{self.doctor_id}'



class Prescriptions(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='prescribed_medication', default=0)
    medication = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)

    def __str__(self):
        return self.medication



class Billing(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='billing')
    total_amount = models.PositiveSmallIntegerField(default=0)
    paid = models.BooleanField(default=False)
    issued_date = models.DateTimeField(auto_now_add=True)



class Ward(models.Model):
    name = models.CharField(max_length=32)
    TYPE_CHOICES =(
        ('VIP', 'VIP'),
        ('simple', 'Simple'),
    )
    ward_types = models.CharField(choices=TYPE_CHOICES, default='simple', max_length=10)
    capacity = models.PositiveSmallIntegerField(default=0)
    current_occupancy = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_free_seats(self):
        a = self.capacity
        b = self.current_occupancy
        return a - b



class Feedback(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()

    def __str__(self):
        return f'{self.patient}-{self.doctor}'



class Chat(models.Model):
    person = models.ManyToManyField(Profile)
    created_date = models.DateField()



class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='message_images/', null=True, blank=True)
    video = models.FileField(upload_to='message_videos/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
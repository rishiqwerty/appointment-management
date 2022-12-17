from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# - 3 types of users (Admin, Doctor and Patient)
# - Each with Different Access and Viewing/Editing rights
# - Create/Update/View Appointments
# - Create/Update/View Patients
# - JSON API based architecture

class Appointment(models.Model):
    creation_date = models.DateTimeField(auto_now=True)
    modification_date = models.DateTimeField(auto_now=True)
    appointment_number = models.CharField(unique=True, max_length=20)
    appointment_date = models.DateField(null=False)
    appointment_time = models.TimeField(null=False)
    doctorID = models.ForeignKey(User, on_delete=models.CASCADE)
    patientID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_id')
    reason = models.CharField(max_length=200)

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=8,choices=(('DOCTOR', 'Doctor'), ('PATIENT','Patient'),('ADMIN', 'Admin')), default='PATIENT')
    name = models.CharField(max_length=100, null=False)
    details = models.JSONField(null=True)

class Doctor(models.Model):
    user_data = models.ForeignKey(UserData, on_delete=models.CASCADE)
    specialist = models.CharField(max_length=100, null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    

class Patient(models.Model):
    user_data = models.ForeignKey(UserData, on_delete=models.CASCADE)
    age = models.CharField(max_length=100, null=True, blank=True)
    blood_group = models.CharField(null=True, blank=True, max_length=5)
    past_medical_report = models.CharField(max_length=100, null=True, blank=True)


class MedicalReport(models.Model):
    patient_id = models.ForeignKey(UserData, on_delete=models.CASCADE)
    date_of_appointment = models.DateTimeField(null=False)
    prescription = models.TextField(max_length=1000, null=True)
    test_requested = models.JSONField(null=True)
    test_results = models.JSONField(null=True)
    creation_date = models.DateTimeField(auto_now=True)
    modification_date = models.DateTimeField(auto_now=True)
    # date_of_birth = models.CharField(default="2022-1-1", max_length=12, editable=True)
    # profile_pic = models.ImageField(default="spotify.png")
    # cover_pic = models.ImageField(default="wallpaperflare.com_wallpaper.jpg")
    # location = models.CharField(max_length=50, null=True, blank=True)
    # website = models.URLField(max_length=50, null=True, blank=True)
    # created_at = models.DateTimeField(default=timezone.now)
    # follower = models.ManyToManyField(User, related_name="follow")
    # follow_check= models.CharField(max_length= 40, blank=True, default="Follow")
from datetime import datetime, timedelta, time
from django import forms
from appointment.models import UserData
from appointment.models import Doctor, Patient
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from appointment.models import Appointment, MedicalReport
HOUR_CHOICES = []
for x in range(9, 18):
    if x==13:
        continue
    HOUR_CHOICES.append((time(hour=x), '{:02d}:00 '.format(x) + '- {:02d}:00'.format(x+1) ))

def doctors(user_type):
    doc_choices = []
    if user_type=='doc':
        doc = Doctor.objects.all()
    else:
        doc = Patient.objects.all()
    for i in doc:
        user = User.objects.get(id=i.user_data.user.id)
        doc_choices.append((i.user_data.user.id, i.user_data.name))
    return doc_choices

def week_dates():
    dates = [datetime.now().date()+timedelta(days=i) for i in range(7)]
    week_dates = []
    for i in dates:
        if i.weekday() not in (5,6):
            week_dates.append((f'{i}',datetime.strftime(i, '%Y-%m-%d')))
    return week_dates
class SignUpForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=(('DOCTOR', 'Doctor'), ('PATIENT','Patient'),('ADMIN', 'Admin')))
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label='',widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label='')


class AppointmentForm(forms.ModelForm):

    appointment_date = forms.ChoiceField(choices=week_dates())
    appointment_time = forms.ChoiceField(choices=HOUR_CHOICES)
    doctorID = forms.ChoiceField(choices=doctors('doc'))
    reason = forms.CharField(max_length=200)
    class Meta:
        model = Appointment
        fields = ('appointment_date','appointment_time', 'doctorID', 'reason')
        widgets = {'appointment_date':forms.Select(choices=week_dates()),
                    'appointment_time':forms.Select(choices=HOUR_CHOICES),
                }
   
    def clean_doctorID(self):
        doc = User.objects.get(id=self.cleaned_data['doctorID'])
        return doc
        
        # return super().save(commit)

class AppointmentAdminForm(forms.ModelForm):

    appointment_date = forms.ChoiceField(choices=week_dates())
    appointment_time = forms.ChoiceField(choices=HOUR_CHOICES)
    doctorID = forms.ChoiceField(choices=doctors('doc'))
    patientID = forms.ChoiceField(choices=doctors('pat'))
    reason = forms.CharField(max_length=200)
    class Meta:
        model = Appointment
        fields = ('appointment_date','appointment_time', 'doctorID', 'patientID', 'reason')
        widgets = {'appointment_date':forms.Select(choices=week_dates()),
                    'appointment_time':forms.Select(choices=HOUR_CHOICES),
                }
   
    def clean_doctorID(self):
        doc = User.objects.get(id=self.cleaned_data['doctorID'])
        return doc
    
    def clean_patientID(self):
        doc = User.objects.get(id=self.cleaned_data['patientID'])
        return doc
        

class MedicalReportForm(forms.ModelForm):
    prescription = forms.CharField(max_length=1000)
    test_requested = forms.CharField()
    test_results = forms.CharField()
    
    class Meta:
        model = MedicalReport
        fields = [
            'prescription',
            'test_requested',
            'test_results'
        ]

class UserForm(forms.Form):
    location = forms.CharField()
    age = forms.CharField()
    blood_group = forms.CharField()
    
    class Meta:
        fields = [
            'age',
            'blood_group'
            'location'
        ]

class DoctorForm(forms.Form):
    specialist = forms.CharField()
    experience = forms.IntegerField()
    bio = forms.CharField()
    location = forms.CharField()

    class Meta:
        fields = [
            'specialist',
            'experience',
            'bio',
            'location'
        ]
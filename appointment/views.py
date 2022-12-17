from datetime import datetime
from http.client import HTTPResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from appointment.models import Doctor
from django.contrib.auth.models import User
from appointment.forms import AppointmentForm, AppointmentAdminForm
from appointment.forms import SignUpForm, LoginForm
from appointment.models import UserData, Appointment, Patient
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.db.models import Q

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user = form.save()
            print()
            user_type = cd.get('user_type')
            if user_type=='ADMIN':
                user.is_superuser = True
                user.is_staff = True
                user.save()
            name = cd.get('first_name') + cd.get('last_name')
            p = UserData.objects.create(user=user, user_type=user_type, name=name)
            p.save()
            if user_type=='DOCTOR':
                d = Doctor.objects.create(user_data=p)
                d.save()
            elif user_type == 'PATIENT':
                d = Patient.objects.create(user_data=p)
                d.save()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('appoint')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    errors = ''
    if request.user.is_authenticated:
        return redirect("appoint")

    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("get-appoint")
                else:

                    return HTTPResponse("Disabled account")
            errors = '*Invalid Username/Password'

        else:
            # print("Error")
            form = LoginForm()
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form, 'error': errors})

'''
- Appointment creation
- Appointment Delete
- Appointment Update
- Doctor availability based on Appointment
'''
@login_required
def appointment_creation(request):
    errors = ''
    user = User.objects.get(id=request.user.id)
    model = Appointment()
    if user.is_superuser:
        user_type = 'ADMIN'
        form = AppointmentAdminForm(request.POST, instance=request.user)
    else:
        form = AppointmentForm(request.POST, instance=request.user)
        user_data = UserData.objects.get(user=user.id)
        user_type = user_data.user_type
    print(user_type)
    if user_type == 'DOCTOR':
        return render(request, 'logout_disabled.html',{'html':"Doctor, you cant create the appointment ask Admin/create new account", 'url':'../register'})
    if request.method == "POST":
        if form.is_valid():
            cd = form.cleaned_data
            date = cd['appointment_date']
            time = cd['appointment_time']
            doc = User.objects.get(id=cd['doctorID'])
            cause = cd['reason']

            date_numb = date.split('-')
            time_numb = time.split(':')
            appointment_number = f"{doc}{date_numb[0]}{date_numb[1]}{date_numb[2]}{time_numb[0]}"
            if Appointment.objects.filter(appointment_number=appointment_number).exists():
                today = datetime.strptime(date, '%Y-%m-%d')
                d = today.day
                m = today.month
                y = today.year
            
                # Retrieve today's bookings
                today_bookings = Appointment.objects.filter(appointment_date__year=y, appointment_date__month=m, appointment_date__day=d, doctorID=doc.id)
                today_time_slot = today_bookings.values('appointment_time__hour')
                today_time_slot_list = [h['appointment_time__hour'] for h in list(today_time_slot)]
                all_time_slot = [9, 10, 11, 12, 14, 15, 16, 17]

                available_slot = check_free_time(all_time_slot, today_time_slot_list)
                if available_slot: 
                    errors = f"Requested slot is already booked, please choose another time in {available_slot}."
                else:
                    errors = "The are not available slot for this booking today."
            else:
                # user = form.save(commit=True)
                model = Appointment(
                    appointment_number=appointment_number,
                    appointment_date=date,
                    appointment_time=time,
                    doctorID=doc,
                    reason=cause,
                    patientID=user
                )
                model.save()
                print(user)
                # user.refresh_from_db()  # load the profile instance created by the signal
                user_type = form.cleaned_data.get('user_type')
                name = form.cleaned_data.get('name')
                # user.username = request.user
                # user.save()
                return redirect('get-appoint')
    return render(request, "create.html", {"form": form, 'error': errors, 'user_type': user_type})
    
def check_free_time(all_time_slot, today_time_slot):
    remain_slot = []
    for remain in all_time_slot:
        if remain not in today_time_slot:
            remain_slot.append(f'{remain}:00 - {remain+1}:00')
            print(today_time_slot,remain)
    return remain_slot

@login_required
def display_appointments(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        if user.is_superuser:
            user_type = 'ADMIN'
        else:
            user_data = UserData.objects.get(user=user.id)
            user_type = user_data.user_type
        appointments = []
        if user_type == 'DOCTOR':
            query = Appointment.objects.filter(doctorID=user.id)
        elif user_type == 'PATIENT':
            query = Appointment.objects.filter(patientID=user.id)
        else:
            query = Appointment.objects.all()
        
        today_date = datetime.today().date()
        hour = datetime.today().hour
        for i in query:
            appointment = {}
            appointment['patient_name'] = UserData.objects.get(user=i.patientID).name
            appointment['doc_name'] = UserData.objects.get(user=i.doctorID).name
            appointment['appointment_time'] = str(i.appointment_date) + '  ' + str(i.appointment_time)
            appointment['details'] = i.reason
            appointment['appointment_number'] = i.appointment_number
            appointment['appointment_id'] = i.id
            appointment['update'] = i.appointment_date > today_date and i.appointment_time.hour > hour + 2
            appointments.append(appointment)
        print(appointments)
    else:
        print('auth plz')
    return render(request, 'appointment_page.html', {'appointment':appointments, 'user_type': user_type})

@login_required
def update_appointment(request, id):
    errors = ''
    user = User.objects.get(id=request.user.id)
    if user.is_superuser:
        user_type = 'ADMIN'
    else:
        user_data = UserData.objects.get(user=user.id)
        user_type = user_data.user_type
    if user_type != 'ADMIN':
        appointment = Appointment.objects.get(Q(doctorID=user.id) | Q(patientID=user.id), pk=id)
    else:
        appointment = Appointment.objects.get(pk=id)
    obj = get_object_or_404(Appointment, pk=id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=request.user)
        if form.is_valid():
            cd = form.cleaned_data
            doc = User.objects.get(id=cd['doctorID'])
            if Appointment.objects.filter(appointment_number=appointment.appointment_number).exists():
                today = datetime.strptime(cd.get('appointment_date'), '%Y-%m-%d')
                d = today.day
                m = today.month
                y = today.year
                time = datetime.strptime(cd['appointment_time'], '%H:%M:%S').hour
                # Retrieve today's bookings
                today_bookings = Appointment.objects.filter(appointment_date__year=y, appointment_date__month=m, appointment_date__day=d, doctorID=doc.id)
                today_time_slot = today_bookings.values('appointment_time__hour')
                today_time_slot_list = [h['appointment_time__hour'] for h in list(today_time_slot)]
                all_time_slot = [9, 10, 11, 12, 14, 15, 16, 17]

                print(time, '------------', today_time_slot_list)
                if time in all_time_slot and time not in today_time_slot_list: 
                    appointment.appointment_date = cd['appointment_date']
                    appointment.appointment_time = cd['appointment_time']
                    appointment.reason = cd['reason']
                    appointment.doctorID = doc
                    appointment.save()
                    return redirect('get-appoint')
                else:
                    available_slot = check_free_time(all_time_slot, today_time_slot_list)
                    errors = f"Requested slot is already booked, please choose another time in {available_slot}."
    else:
        form = AppointmentForm(instance=obj)

    return render(request, "update.html", {"form": form, 'doc':obj, 'error': errors, 'user_type': user_type})

@login_required
def appointment_delete(request, id):
    user = User.objects.get(id=request.user.id)
    if user.is_superuser:
            user_type = 'ADMIN'
    else:
        user_data = UserData.objects.get(user=user.id)
        user_type = user_data.user_type
    if user_type == 'DOCTOR':
        obj = get_object_or_404(Appointment, pk=id, doctorID=user.id)
        obj.delete()
    elif user_type == 'PATIENT':
        obj = get_object_or_404(Appointment, pk=id, patientID=user.id)
        obj.delete()
    else:
        obj = get_object_or_404(Appointment, pk=id)
        obj.delete()
    
    return redirect("get-appoint")

def user_logout(request):
    logout(request)
    return render(request, "login.html")
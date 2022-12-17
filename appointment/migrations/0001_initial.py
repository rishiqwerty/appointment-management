# Generated by Django 4.1.4 on 2022-12-16 16:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('DOCTOR', 'Doctor'), ('PATIENT', 'Patient'), ('ADMIN', 'Admin')], default='PATIENT', max_length=8)),
                ('name', models.CharField(max_length=100)),
                ('details', models.JSONField(null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.CharField(blank=True, max_length=100, null=True)),
                ('blood_group', models.CharField(blank=True, max_length=5, null=True)),
                ('past_medical_report', models.CharField(blank=True, max_length=100, null=True)),
                ('user_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appointment.userdata')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_appointment', models.DateTimeField()),
                ('prescription', models.TextField(max_length=1000, null=True)),
                ('test_requested', models.JSONField(null=True)),
                ('test_results', models.JSONField(null=True)),
                ('creation_date', models.DateTimeField(auto_now=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appointment.userdata')),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialist', models.CharField(blank=True, max_length=100, null=True)),
                ('experience', models.IntegerField(blank=True, null=True)),
                ('bio', models.CharField(blank=True, max_length=100, null=True)),
                ('user_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appointment.userdata')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('appointment_number', models.CharField(max_length=20, unique=True)),
                ('appointment_date', models.DateField()),
                ('appointment_time', models.TimeField()),
                ('reason', models.CharField(max_length=200)),
                ('doctorID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('patientID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
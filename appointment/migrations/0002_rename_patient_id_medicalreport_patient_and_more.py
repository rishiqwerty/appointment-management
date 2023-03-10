# Generated by Django 4.1.4 on 2022-12-18 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medicalreport',
            old_name='patient_id',
            new_name='patient',
        ),
        migrations.RemoveField(
            model_name='medicalreport',
            name='date_of_appointment',
        ),
        migrations.AddField(
            model_name='medicalreport',
            name='appointment',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to='appointment.appointment'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='medicalreport',
            name='test_requested',
            field=models.TextField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='medicalreport',
            name='test_results',
            field=models.TextField(max_length=1000, null=True),
        ),
    ]

# Generated by Django 4.1.4 on 2022-12-18 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0002_rename_patient_id_medicalreport_patient_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdata',
            name='details',
        ),
        migrations.AddField(
            model_name='userdata',
            name='location',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

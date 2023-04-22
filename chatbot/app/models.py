from django.db import models

# Create your models here.


class Doctor(models.Model):
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=100)
    working_hours_start = models.TimeField(null=True,blank=True)
    working_hours_end = models.TimeField(null=True,blank=True)
    working_days = models.CharField(max_length=255,null=True)
    about = models.TextField(blank=True)


class Patient(models.Model):
    email = models.EmailField(primary_key=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    birth_date = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=10)
    marital_status = models.CharField(max_length=20)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    medications = models.BooleanField(default=True)
    allergies = models.BooleanField(default=True)


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True,blank=True)
    end_time = models.DateTimeField(null=True,blank=True)

    class Meta:
        unique_together = ('doctor', 'start_time')

from django.db import models
from datetime import timedelta, datetime

class Speciality(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"({self.pk}) {self.name}"
    
    class Meta:
        verbose_name_plural = "Specialities"


class Doctor(models.Model):
    name = models.CharField(max_length=255)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE, null=True)
    about = models.TextField(blank=True)
    price_egp = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_info(self):
        return f"Name: {self.name} \n Specialty: {self.speciality.name} \n Appointment Fees: {self.price_egp} EGP \n About: {self.about} \n"


class WorkingDay(models.Model):
    WEEKDAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name='working_days')
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"({self.pk}) {str(self.doctor)} {self.WEEKDAY_CHOICES[self.weekday][1]} from {self.start_time} to {self.end_time}"

    def get_info(self):
        return f"{self.WEEKDAY_CHOICES[self.weekday][1]} from {self.start_time} to {self.end_time}"

    def get_valid_working_time(self, selected_date):
        available_slots = []
        year, month, day = map(int, selected_date.split('-'))
        selected_date = datetime(year, month, day)
        start_time = datetime.combine(selected_date, self.start_time)
        end_time = datetime.combine(selected_date, self.end_time)
        time_delta = timedelta(minutes=30)
        current_slot = start_time
        while current_slot < end_time:
            available_slots.append(current_slot)
            current_slot += time_delta
        return available_slots


class Patient(models.Model):
    email = models.EmailField(primary_key=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    marital_status = models.CharField(max_length=20)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    medications = models.BooleanField(default=True)
    allergies = models.BooleanField(default=True)


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    paid = models.BooleanField(default=False) # useful for payment extension later

    class Meta:
        unique_together = ('doctor', 'start_time')

    def __str__(self):
        return f"({self.pk}) {str(self.doctor)} {str(self.patient.email)} {self.start_time} {self.end_time}"

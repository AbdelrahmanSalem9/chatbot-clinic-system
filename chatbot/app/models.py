from django.db import models

# TODO: Modify the models to fit your needs
# Add some random # generator for the appointment id
# add price
# Dealing with this random type of time format
# AM/PM or 24h format

class Doctor(models.Model):
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=100)
    about = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_info(self):
        return f"Name: {self.name} \n Specialty: {self.specialty} \n About: {self.about} \n"


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
        return f"{str(self.doctor)} {self.WEEKDAY_CHOICES[self.weekday][1]} from {self.start_time} to {self.end_time}"

    def get_info(self):
        return f"{self.WEEKDAY_CHOICES[self.weekday][1]} from {self.start_time} to {self.end_time}"

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

    class Meta:
        unique_together = ('doctor', 'start_time')

    def __str__(self):
        return f"{str(self.doctor)} {str(self.patient.email)} {self.start_time} {self.end_time}"
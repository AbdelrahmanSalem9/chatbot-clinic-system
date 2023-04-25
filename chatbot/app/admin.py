from django.contrib import admin
from .models import Patient, Doctor, WorkingDay, Appointment

# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(WorkingDay)
admin.site.register(Appointment)

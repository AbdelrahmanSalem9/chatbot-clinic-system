import json
from django.http import JsonResponse
from datetime import timedelta, datetime
from .models import Appointment, Patient, Doctor, Speciality
from datetime import datetime
from django.utils import timezone


class Action:
    def __init__(self, data):
        self.data = json.loads(data)

    def parse(self):
        pass

    def execute(self):
        pass


class AddPatient(Action):

    def __init__(self, data):
        self.data = data

    def parse(self):
        patient_data = {
            'full_name': self.data.get('full_name'),
            'phone': self.data.get('contact_number'),
            'birth_date': self.data.get('date_of_birth'),
            'gender': self.data.get('gender'),
            'marital_status': self.data.get('marital_status'),
            'height': self.data.get('height'),
            'weight': self.data.get('weight'),
            'medications': self.data.get('medications') == 'yes',
            'allergies': self.data.get('allergies') == 'yes',
        }
        return patient_data

    def execute(self, email):
        try:
            patient_data = self.parse()
            patient, created = Patient.objects.get_or_create(
                email=email, defaults=patient_data)
            if not created:
                # Update only the fields that have changed
                fields_to_update = {
                    k: v for k, v in patient_data.items() if v != getattr(patient, k)}
                if fields_to_update:
                    Patient.objects.filter(pk=email).update(**fields_to_update)
        except Exception as e:
            raise Exception("Can't Save Patient Data")


class CreateAppointment(Action):

    def parse(self):
        try:
            return self.data['patient_email'], self.data['doctor_id'], datetime.strptime(self.data['time_slot'], '%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            raise Exception("Can't Parse Data")

    def execute(self):
        patient_email, doctor_id, time_slot = self.parse()
        print(time_slot)  # 2023-05-03 09:00:00
        try:
            doctor = Doctor.objects.get(pk=doctor_id)
            appointment = Appointment(
                doctor=doctor,
                patient=Patient.objects.get(pk=patient_email),
                start_time=time_slot + timedelta(minutes=180),
                end_time=time_slot + timedelta(minutes=210),
            )
            appointment.save()
            return JsonResponse({'message': 'Appointment booked successfully', 'appointment_id': appointment.pk})

        except Exception as e:
            print(e)
            raise Exception("Can't Create Appointment")


class ModifyAppointment(Action):

    def parse(self):
        try:
            return self.data['date'], datetime.strptime(self.data['time_slot'], '%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            raise Exception("Can't Parse Data")

    def execute(self, id):
        try:
            selected_date, time_slot = self.parse()
            print(time_slot, type(time_slot))
            appointment = Appointment.objects.get(pk=id)
            appointment.start_time = time_slot + timedelta(minutes=180)
            appointment.end_time = time_slot + timedelta(minutes=210)
            appointment.save()
            return JsonResponse({'message': 'Appointment modified successfully', 'appointment_id': appointment.pk})
        except Exception as e:
            print(e)
            raise Exception("Can't Modify Appointment")


class DeleteAppointment(Action):
    def parse(self):
        try:
            return self.data['appointment_id'], self.data['doctor_id'], self.data['patient_email']
        except:
            raise Exception("Can't Parse Data")

    def execute(self):
        appointment_id, doctor_id, patient_email = self.parse()
        try:
            appointment = Appointment.objects.select_related('doctor', 'patient').get(
                pk=appointment_id,
                doctor__pk=doctor_id,
                patient__email=patient_email
            )
            appointment.delete()
            return JsonResponse({'message': 'Appointment deleted successfully', 'deleted': True})
        except Exception as e:
            print(e)
            raise Exception("Can't Delete Appointment")

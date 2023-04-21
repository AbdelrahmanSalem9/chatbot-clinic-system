from .models import Doctor


class QueryHandler:
    # def __init__(self, models=models):
    #     self.model = models

    def doctor_query(self, doctor_id=1):
        doctor = Doctor.objects.get(pk=doctor_id)
        return f"Doctor {doctor.name} is a {doctor.specialty} and is available {doctor.availability}"

    def working_hours_query(self, doctor_id=1):
        doctor = Doctor.objects.get(pk=doctor_id)
        return f"{doctor.availability.capitalize()} from 2:00pm to 7:00pm"

    def appointment_query(self):
        return 

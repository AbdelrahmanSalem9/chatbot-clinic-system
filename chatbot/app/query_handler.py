from .models import Doctor, WorkingDay


class QueryHandler:
    def doctor_query(self, user_input):
        doctors = Doctor.objects.all()
        for doctor in doctors:
            if doctor.name.lower() in user_input.lower():
                return f"Name: {doctor.name} Specialty: {doctor.specialty} Working Days: {self._get_working_days(doctor)} About: {doctor.about}"

    def _get_working_days(self, doctor):
        working_days = [WorkingDay.WEEKDAY_CHOICES[day.weekday][1]
                        for day in WorkingDay.objects.filter(doctor=doctor)]
        return " ".join(working_days)

    def working_hours_query(self, doctor_id=1):
        doctor = Doctor.objects.get(pk=doctor_id)
        return f"{doctor.availability.capitalize()} from 2:00pm to 7:00pm"

    def appointment_query(self):
        return f"Sure, I will take you to the appointment page now...", "/appointment"

    def delete_query(self, user_input):
        return f"Sure, I will help you to cancel an appointment now...", "/delete"

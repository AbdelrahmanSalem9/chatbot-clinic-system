from .models import Doctor, WorkingDay, Appointment


class QueryHandler:
    def doctor_query(self, user_input):
        doctors = Doctor.objects.all()
        for doctor in doctors:
            if doctor.name.lower() in user_input.lower():
                return f"{doctor.get_info()} Working days: {self._get_working_days(doctor)}"

    def _get_working_days(self, doctor):
        return " and ".join([str(working_day.get_info()) for working_day in WorkingDay.objects.filter(doctor=doctor)])

    def working_hours_query(self, doctor_id=1):
        pass

    def modify_appointment_query(self, user_input):
        id = user_input[1:]
        try:
            appointment = Appointment.objects.get(pk=id)
            return f"I will help you modfiy you appointment now...", f"/modify/?id={id}"
        except:
            return f"Sorry, I could not find the appointment with id {user_input}. Please try again."

    def new_appointment_query(self):
        return f"Sure, I will take you to the appointment page now...", "/appointment"

    def delete_appointment_query(self, user_input):
        return f"Sure, I will help you to cancel an appointment now...", "/delete"

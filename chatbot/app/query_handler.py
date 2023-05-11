from .models import Doctor, WorkingDay, Appointment
import re


class QueryHandler:
    def doctor_query(self, user_input):
        doctors = Doctor.objects.all()
        for doctor in doctors:
            if doctor.name.lower() in user_input.lower():
                return f"{doctor.get_info()} Working days: {self._get_working_days(doctor)}"
        else:
            return self.speciality_query()

    def _get_working_days(self, doctor):
        return " and ".join([str(working_day.get_info()) for working_day in WorkingDay.objects.filter(doctor=doctor)])

    def modify_appointment_query(self, user_input):
        id = re.search(r'#(\d+)', user_input).group(1)
        if id:
            try:
                appointment = Appointment.objects.get(pk=id)
                return f"I will help you modfiy you appointment now...", f"/change/?id={id}"
            except:
                return f"Sorry, I could not find the appointment with id: {id}. Please try again."
        else:
            return f"Please provide me with the appointment ID."

    def new_appointment_query(self):
        return f"Sure, I will take you to the appointment page now...", "/patient_registeration"

    def delete_appointment_query(self, user_input):
        return f"Sure, I will help you to cancel an appointment now...", "/cancel"

    def speciality_query(self):
        doctors_by_speciality = {}
        doctors = Doctor.objects.all()
        for doctor in doctors:
            if doctor.speciality.name not in doctors_by_speciality:
                doctors_by_speciality[doctor.speciality.name] = []
            doctors_by_speciality[doctor.speciality.name].append(doctor.name)

        return "\n\n".join([f"{speciality}: {self._list_to_string(doctors_by_speciality[speciality])}" for speciality in doctors_by_speciality])

    def _list_to_string(self, list):
        return ", ".join(list)

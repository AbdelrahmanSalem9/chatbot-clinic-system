from datetime import timedelta, datetime
from .models import Appointment


def get_available_slots(doctor, selected_date):
    weekday = datetime.strptime(selected_date, '%Y-%m-%d').weekday()
    working_days = doctor.working_days.filter(
        weekday=weekday)  # to be optimized
    if not working_days.exists():
        return []

    available_slots = working_days.first().get_valid_working_time(selected_date)

    appointments = Appointment.objects.filter(
        doctor=doctor, start_time__date=selected_date)
    booked_slots = set()
    for appointment in appointments:
        start_time = appointment.start_time
        end_time = appointment.end_time
        current_slot = start_time
        while current_slot < end_time:
            booked_slots.add(current_slot.replace(tzinfo=None))
            current_slot += timedelta(minutes=31)
    available_slots = [
        slot for slot in available_slots if slot not in booked_slots]
    return available_slots

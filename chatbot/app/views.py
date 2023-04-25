from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Patient, Doctor, Appointment
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
import json


from .bot import Bot

bot = Bot()


def IndexView(request):
    return render(request, template_name='app/index.html')


def ChatView(request):
    return render(request, template_name='app/chat.html')


@csrf_exempt
def chatbot(request):
    # Get the user's input from the AJAX request
    user_input = request.POST.get('user_input', '')
    # TODO: Implement a more advanced chatbot here

    # Create a bot response
    bot_response = bot.get_response(user_input)

    if isinstance(bot_response, tuple):
        return JsonResponse({'bot_response': bot_response[0], 'link': bot_response[1]})

    # Send the bot response back to the JavaScript file
    return JsonResponse({'bot_response': bot_response, 'link': None})


def appointment(request):
    if request.POST:
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('contact_number')
        birth_date = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        marital_status = request.POST.get('marital_status')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        medications = True if request.POST.get(
            'medications') == 'yes' else False
        allergies = True if request.POST.get('allergies') == 'yes' else False

        # TODO: check if already exists
        patient = Patient(
            full_name=full_name,
            email=email,
            phone=phone,
            birth_date=birth_date,
            gender=gender,
            marital_status=marital_status,
            height=height,
            weight=weight,
            medications=medications,
            allergies=allergies,
        )
        if not Patient.objects.filter(pk=email).exists():
            patient.save()

        return redirect(f'/book_appointment/?email={email}')
    return render(request, template_name='app/appointment.html')


def check_availability(request):
    if request.method == 'GET' and request.GET.get('doctor') and request.GET.get('date'):
        doctor_id = request.GET.get('doctor')
        doctor = Doctor.objects.get(pk=doctor_id)
        selected_day = request.GET.get('date')
        available_time_slots = get_available_slots(doctor, selected_day)

        response_data = {'available_time_slots': available_time_slots}
        return JsonResponse(response_data)


def get_doctors(request):
    doctors = Doctor.objects.all()
    response_data = {'doctors': list(doctors.values())}
    return JsonResponse(response_data)


@csrf_exempt
def book_appointment(request):
    if request.method == 'POST':
        # print(request.POST.get('patient_email'))
        data = json.loads(request.body)
        doctor_id = data['doctor_id']
        selected_date = data['date']
        time_slot = datetime.strptime(
            data['time_slot'], '%Y-%m-%dT%H:%M:%S.%fZ')
        doctor = Doctor.objects.get(pk=doctor_id)
        # print(f"{type(time_slot)} and {time_slot}")
        appointment = Appointment(
            doctor=doctor,
            patient=Patient.objects.get(pk=data['patient_email']),
            start_time=time_slot + timedelta(minutes=120),
            end_time=time_slot + timedelta(minutes=150),
        )
        appointment.save()
        return JsonResponse({'message': 'Appointment booked successfully'})
    # return JsonResponse({'error': 'Invalid request method'})
    else:
        # Display the form to book an appointment
        doctors = Doctor.objects.all()
        context = {
            'doctors': doctors,
            'patient_email': request.GET.get('email'),
        }
        return render(request, 'app/book_appointment.html', context)
    return render(request, template_name='app/book_appointment.html')


# def get_available_slots(doctor, selected_date):
#     weekday = datetime.datetime.strptime(selected_date, '%Y-%m-%d').weekday()
#     working_day = doctor.working_days.filter(weekday=weekday)
#     if not working_day.exists():
#         return []

#     # Get all existing appointments for the doctor on the selected date
#     appointments = Appointment.objects.filter(
#         doctor=doctor,
#         start_time__date=selected_date,
#     ).order_by('start_time').values_list('start_time', 'end_time')
#     # print(appointments)
#     # Generate a set of all existing appointment times
#     appointment_times = set()
#     for start_time, end_time in appointments:
#         current_time = start_time
#         # print(current_time)
#         while current_time.replace(tzinfo=None) < end_time.replace(tzinfo=None):
#             current_time = current_time.replace(tzinfo=None)
#             appointment_times.add(current_time)
#             current_time += timezone.timedelta(minutes=30)
#     # print(f" ------------> {appointment_times} <----------" )
#     print(appointment_times)
#     # Generate a list of all possible time slots for the selected date
#     year, month, day = map(int, selected_date.split('-'))
#     day_start = timezone.datetime.combine(datetime.date(
#         year, month, day), timezone.datetime.min.time())
#     year, month, day = map(int, selected_date.split('-'))
#     day_end = timezone.datetime.combine(datetime.date(
#         year, month, day), timezone.datetime.max.time())
#     time_slots = []
#     current_slot_start = day_start
#     while current_slot_start + timezone.timedelta(minutes=30) <= day_end:
#         current_slot_end = current_slot_start + timezone.timedelta(minutes=30)
#         time_slots.append((current_slot_start, current_slot_end))
#         current_slot_start = current_slot_end
#     # Find the available slots
#     available_slots = []
#     for slot_start, slot_end in time_slots:
#         if slot_start not in appointment_times and slot_end not in appointment_times:
#             available_slots.append(slot_start)
#     return available_slots

def get_available_slots(doctor, selected_date):
    weekday = datetime.strptime(selected_date, '%Y-%m-%d').weekday()
    working_days = doctor.working_days.filter(weekday=weekday)
    if not working_days.exists():
        return []

    available_slots = []
    for working_day in working_days:
        year, month, day = map(int, selected_date.split('-'))
        selected_date = datetime(year, month, day)
        start_time = datetime.combine(selected_date, working_day.start_time)
        end_time = datetime.combine(selected_date, working_day.end_time)
        time_delta = timedelta(minutes=30)
        current_slot = start_time
        while current_slot < end_time:
            available_slots.append(current_slot)
            current_slot += time_delta

    # appointments = .appointments.filter(start_time__date=selected_date)
    appointments = Appointment.objects.filter(
        doctor=doctor, start_time__date=selected_date)
    booked_slots = set()
    for appointment in appointments:
        start_time = appointment.start_time
        end_time = appointment.end_time
        current_slot = start_time
        while current_slot < end_time:
            booked_slots.add(current_slot.replace(tzinfo=None))
            current_slot += time_delta

    print(booked_slots, type(current_slot))
    print(available_slots[0], type(available_slots[0]))
    available_slots = [
        slot for slot in available_slots if slot not in booked_slots]
    return available_slots

def are_same_time(dt1, dt2):
    return 

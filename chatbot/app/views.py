from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Patient, Doctor, Appointment
from django.utils import timezone
from datetime import timedelta, datetime
import json


from .bot import Bot

bot = Bot()


def IndexView(request):
    return render(request, template_name='app/index.html')


def ChatView(request):
    return render(request, template_name='app/chat.html')

# TODO: handle this csrf_exempt


@csrf_exempt
def chatbot(request):
    # Get the user's input from the AJAX request
    user_input = request.POST.get('user_input', '')

    # Create a bot response
    bot_response = bot.get_response(user_input)

    if isinstance(bot_response, tuple):
        return JsonResponse({'bot_response': bot_response[0], 'link': bot_response[1]})

    # Send the bot response back to the JavaScript file
    return JsonResponse({'bot_response': bot_response, 'link': None})


def appointment(request):
    if request.method == 'POST':
        post_data = request.POST
        email = post_data.get('email')
        if not Patient.objects.filter(pk=email).exists():
            patient = Patient(
                full_name=post_data.get('full_name'),
                email=email,
                phone=post_data.get('contact_number'),
                birth_date=post_data.get('date_of_birth'),
                gender=post_data.get('gender'),
                marital_status=post_data.get('marital_status'),
                height=post_data.get('height'),
                weight=post_data.get('weight'),
                medications=post_data.get('medications') == 'yes',
                allergies=post_data.get('allergies') == 'yes',
            )
            patient.save()

        return redirect(f'/book_appointment/?email={email}')

    return render(request, template_name='app/appointment.html')


def check_availability(request):
    if request.method == 'GET':
        doctor_id = request.GET.get('doctor')
        selected_day = request.GET.get('date')
        if doctor_id and selected_day:
            doctor = get_object_or_404(Doctor, pk=doctor_id)
            available_time_slots = get_available_slots(doctor, selected_day)
            return JsonResponse({'available_time_slots': available_time_slots})
    return JsonResponse({'error': 'Invalid request'})


def get_doctors(request):
    if request.method == 'GET':
        doctors = Doctor.objects.all()
        response_data = {'doctors': list(doctors.values())}
        return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid request'})


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

    available_slots = [
        slot for slot in available_slots if slot not in booked_slots]
    return available_slots

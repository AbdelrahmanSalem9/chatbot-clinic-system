from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Patient, Doctor, Appointment
from django.utils import timezone
from datetime import timedelta
import datetime


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
    try:
        bot_response, link = bot.get_response(user_input)
    except:
        link = None
        bot_response = bot.get_response(user_input)

    # Send the bot response back to the JavaScript file
    return JsonResponse({'bot_response': bot_response, 'link': link})


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


def book_appointment(request):
    # print(request.GET.get('email'))
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        doctor = Doctor.objects.get(pk=doctor_id)
        selected_day = request.POST.get('date')
        available_time_slots = get_available_slots(doctor, selected_day)
        context = {'doctors': Doctor.objects.all(
        ), 'available_time_slots': available_time_slots}

        # Create an appointment and add to the database
        # The user should press button to confirm this appointment then redirect to the chat page with the appoinement information

        return render(request, 'app/book_appointment.html', context)
    else:
        # Display the form to book an appointment
        print(request.POST)
        doctors = Doctor.objects.all()
        context = {'doctors': doctors}
        return render(request, 'app/book_appointment.html', context)
    return render(request, template_name='app/book_appointment.html')


def get_available_slots(doctor, selected_date):
    weekday = datetime.datetime.strptime(selected_date, '%Y-%m-%d').weekday()
    working_day = doctor.working_days.filter(weekday=weekday)
    if not working_day.exists():
        return []

    # Get all existing appointments for the doctor on the selected date
    appointments = Appointment.objects.filter(
        doctor=doctor,
        start_time__date=selected_date,
    ).order_by('start_time').values_list('start_time', 'end_time')

    # Generate a set of all existing appointment times
    appointment_times = set()
    for start_time, end_time in appointments:
        current_time = start_time
        while current_time < end_time:
            appointment_times.add(current_time)
            current_time += timezone.timedelta(minutes=30)

    # Generate a list of all possible time slots for the selected date
    year, month, day = map(int, selected_date.split('-'))
    day_start = timezone.datetime.combine(datetime.date(
        year, month, day), timezone.datetime.min.time())
    day_end = timezone.datetime.combine(datetime.date(
        year, month, day), timezone.datetime.max.time())
    time_slots = []
    current_slot_start = day_start
    while current_slot_start + timezone.timedelta(minutes=30) <= day_end:
        current_slot_end = current_slot_start + timezone.timedelta(minutes=30)
        time_slots.append((current_slot_start, current_slot_end))
        current_slot_start = current_slot_end

    # Find the available slots
    available_slots = []
    for slot_start, slot_end in time_slots:
        if slot_start not in appointment_times and slot_end not in appointment_times:
            available_slots.append(slot_start)

    return available_slots

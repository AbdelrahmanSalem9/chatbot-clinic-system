from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Doctor, Appointment, Speciality
from .utils import get_available_slots
from .actions import CreateAppointment, ModifyAppointment, DeleteAppointment, AddPatient

from .bot import Bot

bot = Bot()


def index_view(request):
    return render(request, template_name='app/index.html')


def chat_view(request):
    return render(request, template_name='app/chat.html')


def chatbot(request):
    # Get the user's input from the AJAX request
    user_input = request.POST.get('user_input', '')

    # Create a bot response
    bot_response = bot.get_response(user_input)

    if isinstance(bot_response, tuple):
        return JsonResponse({'bot_response': bot_response[0], 'link': bot_response[1]})

    # Send the bot response back to the JavaScript file
    return JsonResponse({'bot_response': bot_response, 'link': None})


def patient_registeration(request):
    if request.method == 'POST':
        email = request.POST.get(email)
        AddPatient(request.POST).execute(email)
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
        speciality_id = request.GET.get('speciality')
        if speciality_id:
            doctors = Doctor.objects.filter(speciality=speciality_id)
            response_data = {'doctors': list(doctors.values())}
            return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid request'})


def book_appointment(request):
    if request.method == 'POST':
        return CreateAppointment(request.body).execute()
    else:
        doctors = Doctor.objects.all()
        specialties = Speciality.objects.all()
        context = {
            'doctors': doctors,
            'patient_email': request.GET.get('email'),
            'specialties': specialties,
        }
        return render(request, 'app/book_appointment.html', context)


def cancel(request):
    if request.method == 'POST':
        return DeleteAppointment(request.body).execute()
    else:
        doctors = Doctor.objects.all()
        context = {'doctors': doctors}
        return render(request, template_name='app/delete.html', context=context)


def change(request):
    id = request.GET.get('id')
    if request.method == 'POST':
        return ModifyAppointment(request.body).execute(id)
    else:
        appointment = Appointment.objects.get(pk=id)
        context = {
            'doctors': [appointment.doctor],
            'patient_email': appointment.patient.email,
            'specialties': [appointment.doctor.speciality],
        }
        return render(request, template_name='app/book_appointment.html', context=context)

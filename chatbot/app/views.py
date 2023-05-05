from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Patient, Doctor, Appointment
from django.utils import timezone
from datetime import timedelta, datetime
import json
from .utils import get_available_slots


# TODO: REPLACE JQUERY WITH VANILLA JS





from .bot import Bot

bot = Bot()


def IndexView(request):
    return render(request, template_name='app/index.html')


def ChatView(request):
    return render(request, template_name='app/chat.html')


# TODO: remove the link things


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
        patient_data = {
            'full_name': post_data.get('full_name'),
            'phone': post_data.get('contact_number'),
            'birth_date': post_data.get('date_of_birth'),
            'gender': post_data.get('gender'),
            'marital_status': post_data.get('marital_status'),
            'height': post_data.get('height'),
            'weight': post_data.get('weight'),
            'medications': post_data.get('medications') == 'yes',
            'allergies': post_data.get('allergies') == 'yes',
        }

        patient, created = Patient.objects.get_or_create(
            email=email, defaults=patient_data)
        if not created:
            # Update only the fields that have changed
            fields_to_update = {
                k: v for k, v in patient_data.items() if v != getattr(patient, k)}
            if fields_to_update:
                Patient.objects.filter(pk=email).update(**fields_to_update)

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


# TODO: handle the difference between server local time and the user's local time
# TODO: redirect to error page
def book_appointment(request):
    if request.method == 'POST':
        id = new_appointment(request.body)
        if id:
            return JsonResponse({'message': 'Appointment booked successfully', 'appointment_id': id})
        return JsonResponse({'error': 'Appointment NOT booked'})
    else:
        # Display the form to book an appointment
        doctors = Doctor.objects.all()
        context = {
            'doctors': doctors,
            'patient_email': request.GET.get('email'),
        }
        return render(request, 'app/book_appointment.html', context)


def delete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            appointment = Appointment.objects.select_related('doctor', 'patient').get(
                pk=data['appointment_id'],
                doctor__pk=data['doctor_id'],
                patient__email=data['patient_email']
            )
            appointment.delete()
            return JsonResponse({'message': 'Appointment deleted successfully', 'deleted': 'True'})
        except Appointment.DoesNotExist:
            pass
        return JsonResponse({'error': 'Appointment not found'})

    doctors = Doctor.objects.all()
    context = {'doctors': doctors}
    return render(request, template_name='app/delete.html', context=context)


def new_appointment(data):
    try:
        data = json.loads(data)
        doctor_id = data['doctor_id']
        selected_date = data['date']
        time_slot = datetime.strptime(
            data['time_slot'], '%Y-%m-%dT%H:%M:%S.%fZ')
        doctor = Doctor.objects.get(pk=doctor_id)
        appointment = Appointment(
            doctor=doctor,
            patient=Patient.objects.get(pk=data['patient_email']),
            start_time=time_slot + timedelta(minutes=180),
            end_time=time_slot + timedelta(minutes=210),
        )
        appointment.save()
        return appointment.pk
    except Exception as e:
        print("ERROR is happened when saving new appointment")
        print(e)
        return False


def modify_appointment(request):
    id = request.GET.get('id')
    if request.method == 'POST':
        try:
            appointment = Appointment.objects.get(pk=id)
            data = json.loads(request.body)
            appointment.selected_date = data['date']
            appointment.time_slot = datetime.strptime(
                data['time_slot'], '%Y-%m-%dT%H:%M:%S.%fZ')
            appointment.save()
            return JsonResponse({'message': 'Appointment modified successfully'})
        except Appointment.DoesNotExist:
            return JsonResponse({'message': 'Appointment does not exist'}, status=404)
        except:
            return JsonResponse({'message': 'Failed to modify appointment'}, status=500)
    else:
        appointment = Appointment.objects.get(pk=id)
        context = {
            'doctors': [appointment.doctor],
            'patient_email': appointment.patient.email,
        }
        return render(request, template_name='app/book_appointment.html', context=context)

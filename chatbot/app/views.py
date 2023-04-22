from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Patient

from .bot import Bot

bot = Bot()

# Create your views here.


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
        medications = request.POST.get('medications')
        allergies = request.POST.get('allergies')

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
        patient.save()

        # TODO: redirect to appointment date selection page
        return HttpResponse("Your appointment has been booked successfully")
    return render(request, template_name='app/appointment.html')

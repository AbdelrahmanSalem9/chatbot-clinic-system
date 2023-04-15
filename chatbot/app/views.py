from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def IndexView(request):
    return render(request,template_name='app/index.html')

def ChatView(request):
    return render(request,template_name='app/chat.html')

@csrf_exempt
def chatbot(request):
    # Get the user's input from the AJAX request
    user_input = request.POST.get('user_input', '')

    # TODO: Implement a more advanced chatbot here

    # Create a bot response
    bot_response = 'I got your message: ' + user_input

    # Send the bot response back to the JavaScript file
    return JsonResponse({'bot_response': bot_response})

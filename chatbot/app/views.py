from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def IndexView(request):
    return render(request,template_name='app/index.html')

def ChatbotView(request):
    return render(request,template_name='app/chatbot.html')

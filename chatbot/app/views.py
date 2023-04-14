from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def IndexView(request):
    return HttpResponse("Hello, world. You're at the chatbot index.")

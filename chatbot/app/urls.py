from django.urls import path

from . import views

app_name = "app"
urlpatterns = [
    path('',views.IndexView,name='index'),
    path('chat/',views.ChatView,name='chat'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('appointment/', views.appointment, name='appointment'),
    path('book_appointment/', views.book_appointment, name='book_appointment')
    ]
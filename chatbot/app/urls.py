from django.urls import path

from . import views

app_name = "app"
urlpatterns = [
    path('',views.index_view,name='index'),
    path('chat/',views.chat_view,name='chat'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('patient_registeration/', views.patient_registeration, name='patient_registeration'),
    path('book_appointment/', views.book_appointment, name='book_appointment'),
    path('check_availability/', views.check_availability, name='check_availability'),
    path('get_doctors/', views.get_doctors, name='get_doctors'),
    path('cancel/', views.cancel, name='cancel'),
    path('change/', views.change, name='change'),
    path('get_doctors/', views.get_doctors, name='get_doctors'),
    ]
from django.urls import path

from . import views

app_name = "app"
urlpatterns = [
    path('',views.IndexView,name='index'),
    path('chatbot/',views.ChatbotView,name='chatbot'),
    # path('user/',views.UserView.as_view(),name='user')
    ]
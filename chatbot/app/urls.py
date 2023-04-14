from django.urls import path

from . import views

app_name = "app"
urlpatterns = [
    path('',views.IndexView,name='index'),
    # path('profile/',views.ProfileView,name='profile'),
    # path('user/',views.UserView.as_view(),name='user')
    ]
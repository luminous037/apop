from django.shortcuts import render
from django.contrib.auth.views import LoginView as Login, LogoutView as Logout
from .forms import MyAuthenticationForm

# Create your views here.
class LoginView(Login):
    template_name = 'accounts/login.html'
    redirect_field_name = 'redirect_to'
    next_page= '/'

    
class LogoutView(Logout):
    template_name = 'accounts/login.html'
    redirect_field_name = 'redirect_to'
    next_page = '/'
    
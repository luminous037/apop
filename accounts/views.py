from django.shortcuts import render
from django.contrib.auth.views import LoginView as Login
from .forms import MyAuthenticationForm

# Create your views here.
class LoginView(Login):
    template_name = 'accounts/login.html'
    redirect_field_name = 'redirect_to'
    # form_class = MyAuthenticationForm
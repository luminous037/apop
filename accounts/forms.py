from django import forms
from django.contrib.auth.forms import UserCreationForm

class MyAuthenticationForm(UserCreationForm):
    last_name = forms.CharField(max_length=20, required=True, help_text='성을 입력해 주세요.', label='성')
    first_name = forms.CharField(max_length=20, required=True, help_text='이름을 입력해 주세요.', label='이름')
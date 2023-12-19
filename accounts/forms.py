from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField

class MyAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label="Id",
        widget=forms.TextInput(attrs={"class": 'form-control form-control-lg mb-5', "autofocus": True}),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-lg mb-5", "autocomplete": "current-password"}),
    )
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms

class LoginForm(AuthenticationForm):
    username =  UsernameField(
        label = "Nombre de Usuario",
        widget = forms.TextInput(attrs={'autofocus': True,"class":"form-control"})
        )

    password  = forms.CharField(
        widget=forms.PasswordInput(attrs={"class":"form-control"})
        )
    
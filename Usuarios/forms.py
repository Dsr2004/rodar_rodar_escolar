from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from .models import Carro, Usuario, Hijo

class LoginForm(AuthenticationForm):
    username =  UsernameField(
        label = "Nombre de Usuario",
        widget = forms.TextInput(attrs={'autofocus': True,"class":"form-control","placeholder":"Nombre de usuario"})
        )

    password  = forms.CharField(
        widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Contraseña"})
        )

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['usuario','nombres','apellidos','telefono','email', 'estado', 'hijos']
        widgets = {
            'usuario': forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off"}),
            'nombres': forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off"}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off"}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off"}),
            'email': forms.EmailInput(attrs={'class': 'form-control', "autocomplete": "off"}),
            'hijos': forms.SelectMultiple(attrs={'class': 'form-control', "autocomplete": "off"}),
            'estado': forms.HiddenInput(attrs={'class': 'form-control', "autocomplete": "off"}),

        }

    # def clean_password2(self):
    #     password = self.cleaned_data.get('password')
    #     password2 = self.cleaned_data.get('password2')
    #     if password != password2:
    #         raise forms.ValidationError('Las contraseñas no coinciden')
    #     return password2

class HijoForm(forms.ModelForm):
    class Meta:
        model = Hijo
        fields = "__all__"
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off"}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off"}),
            'latitud': forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off"}),
            'longitud': forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off"}),
            'placa': forms.Select(attrs={'class': 'form-control', "autocomplete": "off"}),
            'placa': forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off"}),
            'posicion': forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off"}),
            'estado': forms.HiddenInput(attrs={'class': 'form-control', "autocomplete": "off"}),
        }

class CarroForm(forms.ModelForm):
    class Meta:
        model = Carro
        fields = "__all__"
        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off"}),
            'nombre_conductor': forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off"}),
            'Marca': forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off"}),
            'color': forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off"}),
            'telefono_conductor': forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off"}),
            'estado': forms.HiddenInput(attrs={'class': 'form-control', "autocomplete": "off"}),

        }



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
    placa = ""
    class Meta:
        model = Hijo
        fields = "__all__"
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off"}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off"}),
            'latitud': forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off"}),
            'longitud': forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off"}),
            'placa': forms.Select(attrs={'class': 'form-control', "autocomplete": "off"}),
            'posicion': forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off"}),
            'estado': forms.HiddenInput(attrs={'class': 'form-control', "autocomplete": "off"}),
        }
    def clean_placa(self):
        self.placa = self.cleaned_data.get("placa")
        return self.placa
    
    def clean_posicion(self):
        posicion = self.cleaned_data.get("posicion")
        return posicion
        
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

class CambiarContrasena(forms.ModelForm):
    password2 = forms.CharField(label="Confirmar contraseña",widget=forms.PasswordInput(
        attrs={
            'id':"confpassword",
            'requerid':'requerid',
            'name':'passwordC',
            "class":"form-control",
        }
    ))
    passwordA = forms.CharField(label="Contraseña antigua",widget=forms.PasswordInput(
        attrs={
            'id':"newpassword",
            'requerid':'requerid',
            'name':'passwordA',
            "class":"form-control",
        }
    ))
    
    class Meta:
        model = Usuario
        
        fields=['password']
        widgets={
            'password': forms.PasswordInput(attrs={'class': 'form-control', "autocomplete": "off",'id':"password",'requerid':'requerid','name':'password',}),
        }
    def clean_password2(self):
        """Validación de contraseña
        
        
        Metodo que valida que ambas contraseñas ingresadas sean iguales, antes de ser encriptadas, Retorna la contraseña Validada.
        """
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('passwordC')
        
        if password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2
    
    def save(self,commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from .models import Usuario

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
        fields = ['usuario','nombres','apellidos','telefono','email', 'estado']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2
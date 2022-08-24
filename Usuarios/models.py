from pyexpat import model
import random
# ***********correo***********
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from statistics import mode
from django.template.loader import render_to_string
# ***********correo***********

from django.db import models
from  django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinLengthValidator
from django.db.models.signals import pre_save

class Carro(models.Model):
    placa = models.CharField(primary_key=True,max_length=10, unique=True)
    nombre_conductor = models.CharField("Nombre del conductor",max_length=150, null=False, blank=False)
    Marca = models.CharField(max_length=50,null=False, blank=False)
    color = models.CharField(max_length=20,null=False, blank=False)
    telefono_conductor = models.CharField("Teléfono del conductor",max_length=10,null=False, blank=False, unique=True)
    estado = models.BooleanField("Estado del carro",default=True,null=False, blank=False)
    
    class Meta:
        db_table = "carros"

    def __str__(self):
        return self.placa
    
class Hijo(models.Model):
    nombres  =models.CharField("Nombre del hijo", blank=False, null=False, max_length=15)
    apellidos = models.CharField("Apellido del hijo", blank=False, null=False, max_length=25)
    latitud = models.FloatField("latitud donde vive",blank=False, null=False) #validacion de minimo 5 caracteres despues del punto
    longitud = models.FloatField("longitud donde vive",blank=False, null=False) 
    placa = models.ForeignKey(Carro, on_delete=models.SET_NULL, null=True, blank=False)
    posicion = models.IntegerField("Posicion del hijo")
    estado = models.BooleanField("Estado del viaje", default=True)
    class Meta:
        db_table = "hijos"

    def __str__(self) -> str:
        return  self.nombres.capitalize() +' '+self.apellidos.lower()

    def get_nombreCompleto(self):
        return self.nombres.capitalize() +' '+self.apellidos.lower()

class UsuarioManager(BaseUserManager):
    def create_user(self,usuario,nombres,apellidos,telefono,email,password=None):
        if  not email:
            raise ValueError('El usuario debe tener un correo electronico!')
        usuario = self.model(
            usuario=usuario, 
            nombres = nombres, 
            apellidos = apellidos,
            telefono = telefono, 
            email = self.normalize_email(email), 
            )
        usuario.set_password(password)
        usuario.save()
        return usuario


    def create_superuser(self,usuario,nombres,apellidos,telefono,email,password=None):
        if  not email:
            raise ValueError('El usuario debe tener un correo electronico!')
        usuario = self.model(
            usuario=usuario, 
            nombres = nombres, 
            apellidos = apellidos,
            telefono = telefono, 
            email = self.normalize_email(email), 
            )
        usuario.set_password(password)
        usuario.administrador = True
        usuario.save()
        return usuario


class Usuario(AbstractBaseUser):
    usuario = models.CharField("Usuario", unique=True, max_length=15)
    nombres  = models.CharField("Nombre de usuario", blank=False, null=False, max_length=15)
    apellidos = models.CharField("Apellido de usuario", blank=False, null=False, max_length=25)
    hijos = models.ManyToManyField(Hijo)
    telefono = models.CharField(max_length=10, validators=[MinLengthValidator(10)])
    email = models.EmailField('Correo Electrónico', unique=True)
    estado = models.BooleanField("Estado del usuario", default=True)
    administrador = models.BooleanField(default=False)
    objects = UsuarioManager()


    USERNAME_FIELD='usuario'
    REQUIRED_FIELDS=["nombres", "apellidos","telefono","email"]

    class Meta:
        db_table = "usuarios"

    def __str__(self):
        return '{}'.format(self.nombres+' '+self.apellidos)

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.administrador
    @property
    def get_nombreCompleto(self):
        return self.nombres.capitalize() +' '+self.apellidos.lower()
 
def pre_save_usuario(sender, instance, *args, **kwargs):
    if instance._state.adding is True:
        instance.estado = True
        if not instance.password:
            minus = 'abcdefghijklmnopqrstuvwxyz'
            mayus = minus.upper()
            numeros = '1234567890'
            simbolos = '!@#$%^&*_+=?/;:'
            longitud = 8
            base = minus + mayus + numeros + simbolos
            muestra = random.sample(base, longitud)
            # password = ''.join(muestra)
            password = "1234"
            instance.set_password(password)

pre_save.connect(pre_save_usuario, sender=Usuario)


# class carro(models.Model):
#     nombre = models.CharField(max_length=120)
#     placa = models.CharField(max_length=6)

#     class Meta:
#         db_table = "CarroPrueba"
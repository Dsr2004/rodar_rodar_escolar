from django.db import models
from  django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinLengthValidator

class Hijo(models.Model):
    nombres  =models.CharField("Nombre del hijo", blank=False, null=False, max_length=15)
    apellido = models.CharField("Apellido del hijo", blank=False, null=False, max_length=25)
    latitud = models.FloatField("latitud donde vive",blank=False, null=False) #validacion de minimo 5 caracteres despues del punto
    longitud = models.FloatField("longitud donde vive",blank=False, null=False) 
    placa = models.CharField("Placa del carro", blank=False, null=False, max_length=6, validators=[MinLengthValidator(6)])
    posicion = models.IntegerField("Posicion del hijo", blank=False, null=False)
    estado = models.BooleanField("Estado del viaje", default=True)
    class Meta:
        db_table = "hijos"

    def __str__(self) -> str:
        return f"{self.nombres} {self.apellido}"


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
    administrador = models.BooleanField(default=False)
    hijos = models.ManyToManyField(Hijo)
    telefono = models.CharField(max_length=10)
    email = models.EmailField('Correo Electrónico', unique=True)
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
 
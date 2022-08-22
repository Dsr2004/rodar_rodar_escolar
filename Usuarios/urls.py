from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('ListarUsuarios/', login_required(Usuarios.as_view()), name='listarUsuarios'),
    path('CrearUsuario/', login_required(CrearUsuario.as_view()), name='crearUsuario'),
    path('VerUsuario/<int:pk>/', login_required(VerUsuario.as_view()), name='verUsuario'),
]
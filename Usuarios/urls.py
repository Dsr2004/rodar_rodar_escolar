from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('ListarUsuarios/', login_required(Usuarios.as_view()), name='listarUsuarios'),
    path('CrearUsuario/', login_required(CrearUsuario.as_view()), name='crearUsuario'),
    path('VerUsuario/<int:pk>/', login_required(VerUsuario.as_view()), name='verUsuario'),
    path('EstadoUsuario/', login_required(EstadoUsuario), name='estadoUsuario'),
    path('EditarUsuario/<int:pk>/', login_required(EditarUsuario.as_view()), name='editarUsuario'),
    path('ListarEstudiantes/', login_required(Estudiantes.as_view()), name='listarEstudiantes'),
    path('CrearEstudiante/', login_required(CrearEstudiante.as_view()), name='crearEstudiante'),
    path('VerEstudiante/<int:pk>/', login_required(VerEstudiante.as_view()), name="verEstudiante"),
    path('EditarEstudiante/<int:pk>/', login_required(EditarEstudiante.as_view()), name='editarEstudiante'),
    path('EstadoEstudiante/', login_required(EstadoEstudiante), name='estadoEstudiante'),
    # Carros
    path('ListarCarros/', login_required(Carros.as_view()), name='listarCarros'),
    path('CrearCarro/', login_required(CrearCarro.as_view()), name='crearCarro'),
    path('EditarCarro/<str:pk>', login_required(EditarCarro.as_view()), name='editarCarro'),
    path('EstadoCarro/', login_required(EstadoCarro), name='estadoCarro'),
]
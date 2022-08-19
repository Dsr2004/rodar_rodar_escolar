from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('ListarUsuarios/', login_required(Usuarios.as_view()), name='listarUsuarios'),
]
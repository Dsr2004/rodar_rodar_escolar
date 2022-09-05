from operator import ge
from webbrowser import get
import pandas as pd
import json
import mygeotab 
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, logout, authenticate  #es para autenticar, iniciar y cerrar la sesión
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import  View, CreateView, ListView, UpdateView, DeleteView, DetailView, TemplateView
from django.db.models import Max
from .forms import HijoForm, LoginForm, UsuarioForm, CarroForm, CambiarContrasena
from .models import Hijo, Usuario, Carro
from .mixins import Directions, if_admin
import os
from dotenv import load_dotenv
load_dotenv()

# localizar la placa
def Locali_placa(Placa):
    api = mygeotab.API(username=os.getenv('Api_username'), password=os.getenv('Api_password'), database=os.getenv('Api_db'))
    api.authenticate()
    Fecha_Leida = datetime.now() + timedelta(hours=5)
    ano = Fecha_Leida.year
    mes = Fecha_Leida.month
    dia = str(Fecha_Leida.day)
    if len(dia) == 1:
        dia = "0" + dia
    hora = str(Fecha_Leida.hour)
    if len(hora) == 1:
        hora = "0" + hora
    minuto = str(Fecha_Leida.minute)
    if len(minuto) == 1:
        minuto = "0" + minuto
    segundo = str(Fecha_Leida.second)
    if len(segundo) == 1:
        segundo = "0" + segundo
    savetime = str(ano) + '-' + str(mes) + '-' + str(dia) + 'T' + str(hora) + ':' + str(minuto) + ':' + str(
        segundo) + ".000Z"
    # devices = api.call('Get', typeName = 'Device')
    # devices = api.call('Get', typeName = 'Device', search={"licensePlate":"DFRL43"})
    # Id_Buscado=devices[0]['id']
    devices = api.call('Get', typeName='Device')
    logs = api.get("LogRecord", search={"fromDate": savetime})
    # logs = api.get("LogRecord", search = {"fromDate": savetime,"deviceSearch": {"id":'bA'}})
    longitud = []
    latitud = []
    Fecha = []
    ID = []
    hora = []
    ##########INICIA MODIFICACIONES#########################################
    placas = []
    Id_Dive = []
    for i in range(len(devices)):
        placas.append(devices[i]['licensePlate'])
        Id_Dive.append(devices[i]['id'])
    for i in range(len(logs)):
        longitud.append(logs[i]['longitude'])
        latitud.append(logs[i]['latitude'])
        Fecha.append((logs[i]['dateTime'] - timedelta(hours=5)).date())
        hora.append((logs[i]['dateTime'] - timedelta(hours=5)).time().strftime('%H:%M:%S'))
        ID.append(logs[i]['device']['id'])
    df_placa = pd.DataFrame({'ID': Id_Dive, 'Placa': placas})
    df = pd.DataFrame({'ID': ID, 'longitud': longitud,
                       'latitud': latitud,
                       'Fecha': Fecha, 'Hora': hora
                       })
    # Se realiza joiner de las dos tablas
    df_cd = pd.merge(df, df_placa, how='inner', on='ID')
    df_cd = df_cd.drop(['ID'], axis=1)
    # Se coloca Df como se espera guardar
    df = df_cd.rename(columns={'Placa': 'ID'})
    df['latitud'][1]
    df['longitud'][1]
    df['ID'][1]
    # df['Tiempo'] = df['Tiempo'].dt.tz_localize(None)
    ##############FIN MODIFICACIONES#######################################
    pos = (list(df["ID"]).index(Placa))
    longitud = df[pos:pos + 1]['longitud'].reset_index(drop=True)[0]
    latitud = df[pos:pos + 1]['latitud'].reset_index(drop=True)[0]
    return longitud, latitud

def index(request):
    usuario = request.user
    hijos = usuario.hijos.all()
    contexto = {"hijos":hijos}
    return render(request, "index.html", contexto)

def Login(request):
    context = {}
    if request.method == "POST":
        form = LoginForm(request,data=request.POST) #con esto se le pasan los datos al formulario, inserción
        if form.is_valid():
            nombre = form.cleaned_data.get("username")
            contrasena = form.cleaned_data.get("password")
            usuario = authenticate(username=nombre, password = contrasena)

            if usuario is not None:
                if usuario.estado == 1:
                    login(request, usuario)
                    if 'next' in request.GET:
                        return redirect(request.GET.get('next'))
                    else:
                        return redirect("index")
                else: 
                    context['error']="Este usuario se encuentra inhabilitado"

        else:
            try:
                Usuario.objects.get(usuario=form.cleaned_data.get('username'))
                context['error']="La contraseña es incorrecta"
            except:
                context['error']="El usuario ingresado no existe"
                
    context['form'] = LoginForm
    return render(request, "login.html", context)

def logout(request):
    logout(request)

def BuscarRuta(request, placa, posicion):
    print(placa)
    print(posicion)
    hijos=Hijo.objects.filter(placa=placa).filter(posicion__lte=posicion)
    hijoBuscado = Hijo.objects.get(placa=placa, posicion=posicion)
    Lat=[]
    Lon=[]
    Pos=[]
    df = pd.DataFrame()
    for hijo in hijos:
        Lat.append(hijo.latitud)
        Lon.append(hijo.longitud)
        Pos.append(hijo.posicion)
    df['Lat'] = Lat
    df['Lon'] = Lon
    df['Pos'] = Pos

    #"---------------------------------"
    # long_a, lat_a= Locali_placa(placa)#inicio

    # long_a = -75.557174
    # lat_a = 6.319017
    long_a = -75.636635
    lat_a = 6.27383
    df = df.append({"Lat":lat_a, "Lon":long_a, "Pos": 0}, ignore_index=True)

    df.sort_values(by=['Pos'], inplace=True)
    df.reset_index(drop=True, inplace=True)

    while len(df) != 11:
        df.loc[len(df)] = [df['Lat'][len(df) - 1],
                           df['Lon'][len(df) - 1], df['Pos'][len(df) - 1]+1]

    #el b es el ultimo de todos los puntos
    lat_b = df.Lat[10]
    long_b = df.Lon[10] #CARRO 10

    #estos son los waipoints
    lat_c = df.Lat[1]
    long_c = df.Lon[1]#CARRO 1
    lat_d = df.Lat[2]
    long_d = df.Lon[2]#CARRO 2
    lat_e = df.Lat[3]
    long_e = df.Lon[3]#CARRO 3
    lat_f = df.Lat[4]
    long_f = df.Lon[4]#CARRO 4
    lat_g = df.Lat[5]
    long_g = df.Lon[5]#CARRO 5
    lat_h = df.Lat[6]
    long_h = df.Lon[6]#CARRO 6
    lat_i = df.Lat[7]
    long_i = df.Lon[7]#CARRO 7
    lat_j = df.Lat[8]
    long_j = df.Lon[8]#CARRO 9
    lat_k= df.Lat[9]
    long_k = df.Lon[9]#CARRO 9

    


    dif_lat = abs(lat_a - lat_k)
    dif_log = abs(long_a - long_k)

    # funcion que cambia el estado de la posicion de un hijo
    if dif_lat < 0.0005 and dif_log < 0.0005:
        Hijo.objects.filter(placa=placa).filter(posicion=posicion).update(estado=False)
        

    if lat_a and lat_b and lat_c and lat_d:
        directions = Directions(
        lat_a= lat_a,
        long_a=long_a,
        lat_b = lat_b,
        long_b=long_b,
        lat_c= lat_c,
        long_c=long_c,
        lat_d = lat_d,
        long_d=long_d,
        lat_e= lat_e,
        long_e=long_e,
        lat_f= lat_f,
        long_f=long_f,
        lat_g = lat_g,
        long_g = long_g, 
        lat_h = lat_h,
        long_h = long_h,
        lat_i = lat_i,
        long_i = long_i,
        lat_j = lat_j,
        long_j = long_j,
        lat_k =  lat_k,
        long_k = long_k 
        )
    context = {
    "google_api_key": settings.API_KEY,
    "lat_a": lat_a,
    "long_a": long_a,
    "lat_b": lat_b,
    "long_b": long_b,
    "lat_c": lat_c,
    "long_c": long_c,
    "lat_d": lat_d,
    "long_d": long_d,
    "lat_e": lat_e,
    "long_e": long_e,
    "lat_f": lat_f,
    "long_f": long_f,
    "lat_g" : lat_g,
    "long_g" : long_g, 
    "lat_h" : lat_h,
    "long_h" : long_h,
    "lat_i" : lat_i,
    "long_i" : long_i,
    "lat_j" : lat_j,
    "long_j" : long_j,
    "lat_k" :  lat_k,
    "long_k" : long_k,
    "origin": f'{lat_a}, {long_a}',
    "destination": f'{lat_b}, {long_b}',
    "directions": directions,
    "placa": placa,
    "posicion":posicion,
    "hijo": hijoBuscado,
    }
   
    return render(request, "mapa.html", context)


def RecargarRuta(request):
    if request.method == "POST":
        placa = request.POST.get('placa')
        posicion = request.POST.get('posicion')
        hijos=Hijo.objects.filter(placa=placa).filter(posicion__lte=posicion)
    hijoBuscado = Hijo.objects.get(placa=placa, posicion=posicion)
    Lat=[]
    Lon=[]
    Pos=[]
    df = pd.DataFrame()
    for hijo in hijos:
        Lat.append(hijo.latitud)
        Lon.append(hijo.longitud)
        Pos.append(hijo.posicion)
    df['Lat'] = Lat
    df['Lon'] = Lon
    df['Pos'] = Pos

    #"---------------------------------"
    # long_a, lat_a= Locali_placa(placa)#inicio

    # long_a = -75.557174
    # lat_a = 6.319017
    long_a = -75.636635
    lat_a = 6.27383
    df = df.append({"Lat":lat_a, "Lon":long_a, "Pos": 0}, ignore_index=True)

    df.sort_values(by=['Pos'], inplace=True)
    df.reset_index(drop=True, inplace=True)

    while len(df) != 11:
        df.loc[len(df)] = [df['Lat'][len(df) - 1],
                           df['Lon'][len(df) - 1], df['Pos'][len(df) - 1]+1]

    #el b es el ultimo de todos los puntos
    lat_b = df.Lat[10]
    long_b = df.Lon[10] #CARRO 10

    #estos son los waipoints
    lat_c = df.Lat[1]
    long_c = df.Lon[1]#CARRO 1
    lat_d = df.Lat[2]
    long_d = df.Lon[2]#CARRO 2
    lat_e = df.Lat[3]
    long_e = df.Lon[3]#CARRO 3
    lat_f = df.Lat[4]
    long_f = df.Lon[4]#CARRO 4
    lat_g = df.Lat[5]
    long_g = df.Lon[5]#CARRO 5
    lat_h = df.Lat[6]
    long_h = df.Lon[6]#CARRO 6
    lat_i = df.Lat[7]
    long_i = df.Lon[7]#CARRO 7
    lat_j = df.Lat[8]
    long_j = df.Lon[8]#CARRO 9
    lat_k= df.Lat[9]
    long_k = df.Lon[9]#CARRO 9

    


    dif_lat = abs(lat_a - lat_k)
    dif_log = abs(long_a - long_k)

    # funcion que cambia el estado de la posicion de un hijo
    if dif_lat < 0.0005 and dif_log < 0.0005:
        Hijo.objects.filter(placa=placa).filter(posicion=posicion).update(estado=False)
        

    if lat_a and lat_b and lat_c and lat_d:
        directions = Directions(
        lat_a= lat_a,
        long_a=long_a,
        lat_b = lat_b,
        long_b=long_b,
        lat_c= lat_c,
        long_c=long_c,
        lat_d = lat_d,
        long_d=long_d,
        lat_e= lat_e,
        long_e=long_e,
        lat_f= lat_f,
        long_f=long_f,
        lat_g = lat_g,
        long_g = long_g, 
        lat_h = lat_h,
        long_h = long_h,
        lat_i = lat_i,
        long_i = long_i,
        lat_j = lat_j,
        long_j = long_j,
        lat_k =  lat_k,
        long_k = long_k 
        )

        context = {
        "google_api_key": settings.API_KEY,
        "lat_a": lat_a,
        "long_a": long_a,
        "lat_b": lat_b,
        "long_b": long_b,
        "lat_c": lat_c,
        "long_c": long_c,
        "lat_d": lat_d,
        "long_d": long_d,
        "lat_e": lat_e,
        "long_e": long_e,
        "lat_f": lat_f,
        "long_f": long_f,
        "lat_g" : lat_g,
        "long_g" : long_g, 
        "lat_h" : lat_h,
        "long_h" : long_h,
        "lat_i" : lat_i,
        "long_i" : long_i,
        "lat_j" : lat_j,
        "long_j" : long_j,
        "lat_k" :  lat_k,
        "long_k" : long_k,
        "origin": f'{lat_a}, {long_a}',
        "destination": f'{lat_b}, {long_b}',
        "directions": directions,
        "placa": placa,
        "posicion":posicion
        }
    
        return JsonResponse(context)

#GESTION DE USUARIOS
class Usuarios(ListView):
    model = Usuario
    template_name = "usuarios.html"
    
    def get(self, request, *args, **kwargs):
        Admin = if_admin(request)
        if Admin == False:
            return redirect("index")
        context = {"usuarios":self.model.objects.filter(administrador=False).exclude(pk = request.user.pk)}
        return render(request, self.template_name,context)

class CrearUsuario(CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = "Usuarios/crear.html"
    success_url = reverse_lazy("listarUsuarios")

    def form_invalid(self, form):
       return JsonResponse({"errores": form.errors}, status=400)

class VerUsuario(DetailView):
    model = Usuario
    template_name = "Usuarios/ver.html"
    context_object_name = "usuario"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hijos'] = Hijo.objects.filter(usuario=self.object)
        return context

class EditarUsuario(UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = "Usuarios/editar.html"
    success_url = reverse_lazy("listarUsuarios")

    def post(self, request, *args, **kwargs):
        post = request.POST.copy()
        post["usuario"] = self.get_object().usuario
        form = self.form_class(post, instance=self.get_object())
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)

    def form_invalid(self, form):
        print(form.errors)
        return JsonResponse({"errores": form.errors}, status=400)

def EstadoUsuario(request):
    if request.method == "POST":
        usuario = Usuario.objects.get(pk=request.POST.get('pk'))
        if usuario.estado:
            usuario.estado = False
            usuario.save()
            return JsonResponse({"succes":"Se ha inhabilitado el usuario correctamente"}, status=200)    
        
        else:
            usuario.estado = True
            usuario.save()
            return JsonResponse({"success":"Se ha habilitado el usuario correctamente"},status=200)

class Estudiantes(ListView):
    model = Hijo
    template_name = "estudiantes.html"
    
    def get(self, request, *args, **kwargs):
        Admin = if_admin(request)
        if Admin == False:
            return redirect("index")
        context = {"hijos":self.model.objects.all().order_by("-estado")}
        return render(request, self.template_name,context)

class CrearEstudiante(CreateView):
    model = Hijo
    form_class = HijoForm
    template_name = "Estudiantes/crear.html"
    success_url = reverse_lazy("listarEstudiantes")

    def form_invalid(self, form):
        errores =  form.errors
        return JsonResponse({"errores": errores}, status=400)

class VerEstudiante(DetailView):
    model = Hijo
    template_name = "Estudiantes/ver.html"
    context_object_name = "estudiante"

class EditarEstudiante(UpdateView):
    model = Hijo
    form_class = HijoForm
    template_name = "Estudiantes/editar.html"
    success_url = reverse_lazy("listarEstudiantes")

def EstadoEstudiante(request):
    if request.method == "POST":
        estudiante = Hijo.objects.get(pk=request.POST.get('pk'))
        if estudiante.estado:
            estudiante.estado = False
            estudiante.save()
            return JsonResponse({"succes":"Se ha inhabilitado el estudiante correctamente"}, status=200)    
        
        else:
            estudiante.estado = True
            estudiante.save()
            return JsonResponse({"success":"Se ha habilitado el estudiante correctamente"},status=200)

# Gestión Carros
class Carros(ListView):
    model = Carro
    template_name = "carros.html"
    
    def get(self, request, *args, **kwargs):
        Admin = if_admin(request)
        if Admin == False:
            return redirect("index")
        context = {"carros":self.model.objects.all()}
        return render(request, self.template_name,context)

class CrearCarro(CreateView):
    model = Carro
    form_class = CarroForm
    template_name = "Carros/crear.html"
    success_url = reverse_lazy("listarCarros")

    def form_invalid(self, form):
        print(form.errors)
        return JsonResponse({"errores": form.errors}, status=400)
    
class EditarCarro(UpdateView):
    model = Carro
    form_class = CarroForm
    template_name = "Carros/editar.html"
    success_url = reverse_lazy("listarCarros")

def EstadoCarro(request):
    if request.method == "POST":
        carro = Carro.objects.get(placa=request.POST.get('placa'))
        if carro.estado:
            carro.estado = False
            carro.save()
            return JsonResponse({"succes":"Se ha inhabilitado el carro correctamente"}, status=200)    
        
        else:
            carro.estado = True
            carro.save()
            return JsonResponse({"success":"Se ha habilitado el carro correctamente"},status=200)


class Rutas(ListView):
    model=Carro
    template_name="rutas.html"
    context_object_name = "carros"

    def post(self, request, *args, **kwargs):
        placa = request.POST.get("placa")
        estudiantes = Hijo.objects.filter(placa=placa).order_by("posicion")
        ctx={"estudiantes":estudiantes}
        ctx["placa"]=placa
        return render(request, "Rutas/rutaEstudiantes.html", ctx)

class AgregarEstudianteRuta(View):
    def get(self, request, *args, **kwargs):
        placa = kwargs["placa"]
        estudiantes = Hijo.objects.filter(placa=None).exclude(placa=placa)
        ctx={"estudiantes":estudiantes, "placa":placa}
        return render(request, "Rutas/agregarEstudiante.html", ctx)

    def post(self, request, *args, **kwargs):
        placa = request.POST.get("placa", "")
        carro = Carro.objects.get(placa=placa)
        estudiante = request.POST.get("estudiante", "")
        estudianteMayor = Hijo.objects.filter(placa=placa)
        if estudianteMayor:
            estudianteMayor = estudianteMayor.aggregate(Max("posicion"))
            estudianteMayor = estudianteMayor['posicion__max']
        else:
            estudianteMayor = 0

        if placa != "" or estudiante != "":
            estudiante = Hijo.objects.get(pk=estudiante)
            estudiante.placa = carro
            estudiante.posicion = estudianteMayor+1
            estudiante.save()

            return JsonResponse({"correcto":"Se agregao al carro"}, status=200)

        else: 
            return JsonResponse({"error":"No hay placa o estudiante"}, status=400)

class QuitarEstudianteRuta(View):
    def post(self, request, *args, **kwargs):
        estudiante = request.POST.get("id", "")
        if estudiante != "":
            estudiante = Hijo.objects.get(pk=estudiante)
            estudiante.placa = None
            estudiante.posicion = None
            estudiante.save()

            return JsonResponse({"correcto":"Se removio al carro"}, status=200)
        else: 
            return JsonResponse({"error":"No hayo estudiante"}, status=400)


class CambiarEstudiantesRuta(View):
    model=Hijo
    template_name="Rutas/cambiarRutaEstudiantes.html"
    context_object_name = "carros"

    def get(self, request, *args, **kwargs):
        placa = kwargs["placa"]
        estudiantes = self.model.objects.filter(placa=placa)
        ctx = {"estudiantes":estudiantes,"placa":placa}
        return render(request, self.template_name, ctx)
    
    def post(self, request, *args, **kwargs):
        x = request.POST.getlist("datos[]")
        datos = json.loads(x[0])
        for datos in datos:
            print(datos)
            estudiante = self.model.objects.get(pk=datos["pk"])
            print(estudiante)
            estudiante.posicion = datos["posicion"]
            print(estudiante.posicion)
            estudiante.save()
        return JsonResponse({"correcto":"hola"}, status=200)

class CambiarContrasena(TemplateView):
    model = Usuario
    form_class = CambiarContrasena
    template_name="Usuarios/CambiarContrasena.html" 
    
    def get(self, request, *args, **kwargs):
        contexto={"form":self.form_class}
        return render(request, self.template_name, contexto)
    def post(self, request, *args, **kwargs):
        password = request.POST.get('contraseña')
        password2 = request.POST.get('contraseñaC')
        passwordA = request.POST.get('contraseñaA')
        if password == password2:
            if password != passwordA:
                username= request.user.usuario
                user = authenticate(username=username, password=passwordA)
                if user is not None:
                    user.set_password(password)
                    user.save()
                    return JsonResponse({"success":"Succes"})
                else:
                    data = json.dumps({'error': 'La contraseña antigua no es correcta'})
                    return HttpResponse(data, content_type="application/json", status=400)
            else:
                data = json.dumps({'error': 'La nueva contraseña no puede ser igual a la antigua'})
                return HttpResponse(data, content_type="application/json", status=400)
        else:
            data = json.dumps({'error': 'Las contraseñas no coinciden'})
            return HttpResponse(data, content_type="application/json", status=400)
        
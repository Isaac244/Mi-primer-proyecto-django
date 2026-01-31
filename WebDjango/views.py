from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render
#FUNCIONALIDAD DE LOGIN
from django.contrib.auth import login as lg
#Autenticar con login
from django.contrib.auth import authenticate
#Redireccionar a pagina principal
from django.shortcuts import redirect
#Mostrar mensajes de login
from django.contrib import messages
#FUNCIONALIDAD DE LOGOUT
from django.contrib.auth import logout
#Traer form del registro
from .forms import Registro
#ENCRIPTAR LA CONTRASEÑA DEL USUARIO
#from django.contrib.auth.models import User
#OBTENER LOS PRODUCTOS DESDE LA BASE DE DATOS
from products.models import Product
#REDIRIGIR A PESTAÑA DE URL SELECCIONADO DESPUES DE LOGIN
from django.http import HttpResponseRedirect
#ASIGNAR EL USUARIO NUESTRO SIN EL DE DJANGO
from users.models import User

def index(request):
    productos = Product.objects.all()
    return render(request, 'index.html', {
        'mensaje' : 'Tienda',
        'titulo' : 'Inicio',
        'productos' : productos,
    })

#LOGIN HTML
def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        usuarios = authenticate(username=username, password=password)
        if usuarios:
            lg(request, usuarios)
            messages.success(request, f'Bienvenido estimado {usuarios.username}')

            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET['next'])

            return redirect('index')
        else:
            messages.error(request, 'Datos incorrectos')

    return render(request, 'users/login.html', {})

#LOGOUT
def salir(request):
    logout(request)
    messages.success(request, 'Sesion cerrada')
    return redirect(login)

#REGISTRO
def registro(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = Registro(request.POST or None)
    if request.method=='POST' and form.is_valid():
        

        usuario = form.save()
        if usuario:
            lg(request, usuario)
            messages.success(request, f'Bienvenido estimado {usuario.username}')
            return redirect('index')
        
    return render(request, 'users/registro.html', {
        'form' : form
    })
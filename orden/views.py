from django.shortcuts import redirect, render, get_object_or_404
from carts.funciones import funcionCarrito
from .models import Orden
from .utils import funcionOrden
from django.contrib.auth.decorators import login_required
from .utils import breadcrumb
from DirEnvio.models import DireccionEnvio

# Create your views here.
@login_required(login_url='login')
def orden(request):
    cart = funcionCarrito(request)
    orden = funcionOrden(cart, request)

    return render(request, 'orden/orden.html', {
        'cart': cart,
        'orden': orden,
        'breadcrumb': breadcrumb()
    })


@login_required(login_url='login')
def direccion(request):
    cart = funcionCarrito(request)
    orden = funcionOrden(cart, request)

    direccion_envio = orden.get_or_set_direccion_envio()
    contDireccion = request.user.direccionenvio_set.count() > 1

    return render(request, 'orden/direccion.html', {
        'cart' : cart,
        'orden' : orden,
        'direccion_envio' : direccion_envio,
        'contDireccion' : contDireccion,
        'breadcrumb' : breadcrumb(address=True),
    })


@login_required(login_url='login')
def select_direccion(request):
    direccion_envios = request.user.direccionenvio_set.all()
    return render(request, 'orden/select_direccion.html', {
        'breadcrumb' : breadcrumb(address=True),
        'direccion_envios' : direccion_envios,
    })

@login_required(login_url='login')
def check_direccion(request, pk):
    cart = funcionCarrito(request)
    orden = funcionOrden(cart, request)

    direccion_envio = get_object_or_404(DireccionEnvio, pk=pk)

    if request.user.id != direccion_envio.user_id:
        return redirect('index')
    
    orden.update_direccion_envio(direccion_envio)

    return redirect('direccion')
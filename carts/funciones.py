from .models import Cart

def funcionCarrito(request):
    #print(dir(request.session))
    #request.session.set_expiry(300) Este elemento nos permite conocer el limite maximo para carrito. El numero es 5 minutos
    #'session_key', 'set_expiry'
    #key = request.session.session_key
    #print(key)
    user = request.user if request.user.is_authenticated else None
    cart_id = request.session.get('cart_id')
    cart = Cart.objects.filter(cart_id=cart_id).first()

    if cart is None:
        cart = Cart.objects.create(user=user)
    
    if user and cart.user is None:
        cart.user = user
        cart.save()
    
    request.session['cart_id'] = cart.cart_id

    return cart


def deleteCart(request):
    request.session['cart_id'] = None
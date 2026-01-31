from django.db import models
from users.models import User
from products.models import Product
from django.db.models.signals import pre_save, post_save
from django.db.models.signals import m2m_changed
import uuid
import decimal

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartProduct')
    subtotal = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    total = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    FEE = 0.01

    def __str__(self):
        return self.cart_id

    def update_totals(self):
        self.update_subtotal()
        self.update_total()
        
        if self.orden:
            self.orden.update_total()

    def update_subtotal(self):
        self.subtotal = sum([
            i.quantity * i.product.price for i in self.product_related()
        ])
        self.save()

    def update_total(self):
        self.total = self.subtotal + (self.subtotal * decimal.Decimal(Cart.FEE))
        self.save()

    def product_related(self):
        return self.cartproduct_set.select_related('product')
    
    @property
    def orden(self):
        return self.orden_set.first()

#Clase para actualizar los totales en models
class CartProductManager(models.Manager):
    
    def crearActualizar(self, cart, product, quantity=1):
        object, created = self.get_or_create(cart=cart, product=product)

        if not created:
            quantity = object.quantity + quantity
            
        object.update_quantity(quantity)
        return object

#Clase para la inclusiond de cantidad
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CartProductManager()

    def update_quantity(self, quantity=1):
        self.quantity = quantity
        self.save()

#Funcion de incluir el carrito
def set_cart_id(sender, instance, *args, **kwargs):
    if not instance.cart_id:
        instance.cart_id = str(uuid.uuid4())

#Funcion de calcular los totales del carrito
def update_totals(sender, instance, action,*args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        instance.update_totals()

#Funcion para mostrar los post actualizados
def post_actualizar(sender, instance, *args, **kwargs):
    instance.cart.update_totals()

post_save.connect(post_actualizar, sender=CartProduct)
pre_save.connect(set_cart_id, sender=Cart)
m2m_changed.connect(update_totals, sender=Cart.products.through)
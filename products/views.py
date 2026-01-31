from django.shortcuts import render

from .models import Product
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q

#Listado de productos
class ProductListView(ListView):
    template_name = 'index.html'
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mensaje'] = 'Productos'
        return context

#Detalle de cada lista
class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
#Buscador de los productos
class ProductSearchListView(ListView):
    template_name = 'products/search.html'

    def get_queryset(self):
        filters = Q(title__icontains=self.query()) | Q(category__title__icontains=self.query())
        return Product.objects.filter(filters)
    
    def query(self):
        return self.request.GET.get('i')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query()
        return context
from django import template

#Incluir decorador al signo de los precios
register = template.Library()

@register.filter()
def precio_tag(value):
    return '${0:.2f}'.format(value)
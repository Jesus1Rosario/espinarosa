# crud_app/templatetags/filtros_personalizados.py

from django import template

register = template.Library()

@register.filter
def multiplicar(valor, cantidad):
    return valor * cantidad

@register.filter
def formato_precio(value):
    """ Formatear números con puntos como separadores de miles """
    try:
        return '{:,.0f}'.format(value).replace(',', '.')
    except (ValueError, TypeError):
        return value
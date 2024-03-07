import django_filters 
from django import forms
from sasg.models import Producto

class ProductoFilter(django_filters.FilterSet):
    cantidad = django_filters.CharFilter(lookup_expr='icontains', label='Cantidad')
    nomproducto = django_filters.CharFilter(lookup_expr='icontains', label='Nombre del producto')
    nomcategoria = django_filters.CharFilter(lookup_expr='exact', label='Categoría')

    class Meta:
        model = Producto
        fields = ['cantidad', 'nomproducto', 'nomcategoria']
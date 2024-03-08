import django_filters 
from django import forms
from sasg.models import Producto

class ProductoFilter(django_filters.FilterSet):
    cantidad = django_filters.CharFilter(
        lookup_expr='icontains', 
        label='Cantidad',
        widget=forms.TextInput(attrs={'placeholder': 'Buscar', 'class': 'form-control'})
    )
    nomproducto = django_filters.CharFilter(
        lookup_expr='icontains', 
        label='Nombre del producto',
        widget=forms.TextInput(attrs={'placeholder': 'Buscar', 'class': 'form-control'})
    )
    nomcategoria = django_filters.CharFilter(
        lookup_expr='exact', 
        label='Categoría',
        widget=forms.TextInput(attrs={'placeholder': 'Buscar', 'class': 'form-control'})
    )
    idproducto = django_filters.CharFilter(
        lookup_expr='icontains', 
        label='Id Producto',
        widget=forms.TextInput(attrs={'placeholder': 'Buscar', 'class': 'form-control'})
    )
    fecharegistro = django_filters.CharFilter(
        lookup_expr='icontains', 
        label='Fecha Registro',
        widget=forms.DateInput(attrs={'placeholder': 'Buscar', 'class': 'form-control'})
    )


    class Meta:
        model = Producto
        fields = ['cantidad', 'nomproducto', 'nomcategoria', 'idproducto', 'fecharegistro']
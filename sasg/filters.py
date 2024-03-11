import django_filters 
from django import forms
from .models import Producto, Venta, Pedido, Compra, Usuarios


#-------------FILTRO DE PRODUCTOS-------------------------------
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
        
        
#-----------------FILTRO DE VENTAS------------------


class VentaFilter(django_filters.FilterSet):
    idventa = django_filters.NumberFilter(
        lookup_expr='icontains',
        label='ID Venta',
        widget=forms.NumberInput(attrs={'placeholder': 'Buscar', 'class': 'form-control'})
    )
    fechaemision = django_filters.DateFilter(
        lookup_expr='exact', 
        label='Fecha de Emision',
        widget=forms.DateInput(attrs={'placeholder': 'Buscar', 'class': 'form-control'})
    )
    idpedido = django_filters.CharFilter(
        lookup_expr='exact', 
        label='Id Pedido',
        widget=forms.TextInput(attrs={'placeholder': 'Buscar', 'class': 'form-control'})
    )
    idcliente = django_filters.CharFilter(
        lookup_expr='exact', 
        label='Id Cliente',
        widget=forms.TextInput(attrs={'placeholder': 'Buscar', 'class': 'form-control'})
    )
    producto = django_filters.CharFilter(
        lookup_expr='icontains', 
        label='Producto',
        widget=forms.TextInput(attrs={'placeholder': 'Buscar', 'class': 'form-control'})
    )
    cantidad = django_filters.NumberFilter(
        lookup_expr='exact', 
        label='Cantidad',
        widget=forms.NumberInput(attrs={'placeholder': 'Buscar', 'class': 'form-control'})
    )

    class Meta:
        model = Venta
        fields = ['idventa', 'fechaemision', 'idpedido', 'idcliente', 'producto', 'cantidad']

#------------------FILTRO DE PEDIDOS----------------------

class PedidoFilter(django_filters.FilterSet):
    idpedido = django_filters.NumberFilter(
        lookup_expr='icontains',
        label='ID Pedido',
        widget=forms.NumberInput(attrs={'placeholder': 'Buscar', 'class': 'form-control'})
    )
    idusuario = django_filters.NumberFilter(
        lookup_expr='exact',
        label='Id Usuario',
        widget=forms.NumberInput(attrs={'placeholder': 'Buscar', 'class': 'form-control'})
    )
    fechaemision = django_filters.DateFilter(
        lookup_expr='exact',
        label='Fecha de Emision',
        widget=forms.DateInput(attrs={'placeholder': 'Buscar', 'class': 'form-control'})
    )
    estado = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Estado',
        widget=forms.TextInput(attrs={'placeholder': 'Buscar', 'class': 'form-control'})
    )
    class Meta:
        model = Pedido
        fields = ['idpedido', 'idusuario', 'fechaemision', 'estado']
    
#-----------------FILTRO COMPRAS--------------

class CompraFilter(django_filters.FilterSet):
    idcompra  = django_filters.NumberFilter(
        lookup_expr='icontains',
        label='ID Compra',
        widget=forms.NumberInput(attrs={'placeholder': 'Buscar', 'class': 'form-control'})
    )
    fechaemision = django_filters.DateFilter(
        lookup_expr='icontains',
        label='Fecha de Emision',
        widget=forms.DateInput(attrs={'placeholder': 'Buscar', 'class': 'form-control'})
    )
    idproveedor  = django_filters.NumberFilter(
        lookup_expr='icontains',
        label='Id Proveedor',
        widget=forms.DateInput(attrs={'placeholder': 'Buscar', 'class': 'form-control'})
    )
    class Meta:
        model = Compra
        fields = ['idcompra', 'fechaemision', 'idproveedor']
        
#-----------------FILTRO USUARIOS-----------------

class UsuariosFilter(django_filters.FilterSet):
    idusuario = django_filters.NumberFilter(
        lookup_expr='icontains',
        label='ID Usuario',
        widget=forms.NumberInput(attrs={'placeholder': 'Buscar', 'class': 'form-control'})
    )
    rol = django_filters.NumberFilter(
        lookup_expr='exact',
        label='Rol',
        widget=forms.NumberInput(attrs={'placeholder': 'Buscar', 'class': 'form-control'})
    )
    nombres = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Nombres',
        widget=forms.TextInput(attrs={'placeholder': 'Buscar', 'class': 'form-control'})
    )
    apellidos = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Apellidos ',
        widget=forms.TextInput(attrs={'placeholder': 'Buscar', 'class': 'form-control'})
    )
    
    estado = django_filters.CharFilter(
        lookup_expr='exact',
        label='Estado',
        widget=forms.TextInput(attrs={'placeholder': 'Buscar', 'class': 'form-control'})
    )
    class Meta:
        model = Usuarios
        fields = ['idusuario', 'rol', 'nombres' , 'apellidos', 'estado']
    

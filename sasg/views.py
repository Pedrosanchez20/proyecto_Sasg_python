import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render

from .models import Pedido, Producto, Usuarios, Venta, Proveedor


# Create your views here.
def asagoView(request):
    return render(request, 'sasg/index.html')

def catCarnView(request):
    return render(request, 'sasg/catcarne.html')

def catPollView(request):
    return render(request, 'sasg/catpollo.html')

def catCerdView(request):
    return render(request, 'sasg/catcerdo.html')

def catChoView(request):
    return render(request, 'sasg/catchorizo.html')

def prodView(request):
    producto = Producto.objects.all()
    data={
        'producto':producto,
    }
    return render(request, 'sasg/productos.html',data)

def pedView(request):
    pedido = Pedido.objects.all()
    data={
        'pedido':pedido,
    }
    return render(request, 'sasg/pedidos.html',data)

def ventView(request):
    venta = Venta.objects.all()
    data={
        'venta': venta,
    }
    return render(request, 'sasg/ventas.html',data)

def usuaView(request):
    usuarios = Usuarios.objects.all()
    data={
        'usuarios': usuarios,
    }
    return render(request, 'sasg/usuarios.html',data)

#proveedores

def proveesView(request):
    proveedores = Proveedor.objects.all()
    data={
        'proveedores': proveedores,
    }
    return render(request, 'sasg/proveedores.html',data)

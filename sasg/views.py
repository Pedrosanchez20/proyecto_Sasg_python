import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render

from .models import Pedido, Producto, Usuarios, Venta, Roles, Proveedor

# Create your views here.
def sasg(request):
    return render(request, 'sasg/index.html')

def catCarnView(request):
    return render(request, 'sasg/catcarne.html')

def catPollView(request):
    return render(request, 'sasg/catpollo.html')

def catCerdView(request):
    return render(request, 'sasg/catcerdo.html')

def catChoView(request):
    return render(request, 'sasg/catchorizo.html')

#--------------------USUARIOS----------------------------

def registrar_usuario(request):
    if request.method== 'POST':
        idusuario=request.POST.get('idusuario')
        idrol=request.POST.get('rol')
        nombres=request.POST.get('nombres')
        apellidos=request.POST.get('apellidos')
        fechanacimiento=request.POST.get('fechanacimiento')
        direccion=request.POST.get(' direccion')
        telefono=request.POST.get('telefono')
        email=request.POST.get('email')
        contrasena=request.POST.get('contrasena')
        estado=request.POST.get('estado')
        
        usuario = Usuarios(
            idusuario=idusuario,
            nombres=nombres,
            apellidos=apellidos,
            fechanacimiento=fechanacimiento,
            direccion=direccion,
            telefono=telefono,
            email=email,           
            contrasena=contrasena,
            estado=estado,            
            rol=Roles.objects.get(idrol=idrol),
        )
        
        usuario.save()
    return render(request, "personas/editar.html")

def listar_usuario(reques):
    usuarios = Usuarios.objects.all()
    data={
        'usuarios':usuarios,
    }
    return render(reques,'sasg/usuarios.html',data)

#--------------------PRODUCTOS----------------------------

def listar_producto(request):
    producto = Producto.objects.all()
    data={
        'producto':producto,
    }
    return render(request, 'sasg/productos.html',data)

def registrar_producto(request):
    if request.method== 'POST':
        idproducto=request.POST.get('idproducto')
        fecharegistro=request.POST.get('fecharegistro')
        nomproducto=request.POST.get('nomproducto') 
        nomcategoria=request.POST.get('nomcategoria') 
        cantidad=request.POST.get('cantidad') 
        fechavencimiento=request.POST.get('fechavencimiento') 
        valorlibra=request.POST.get('valorlibra') 
        producto = Producto(
            idproducto= idproducto,
            fecharegistro= fecharegistro,
            nomproducto= nomproducto,
            nomcategoria= nomcategoria,
            cantidad= cantidad,
            fechavencimiento= fechavencimiento,
            valorlibra= valorlibra,
        )
        
        producto.save()
    return redirect("listar_productos")
def pre_editar_producto(request,idproducto):
    producto=Producto.objects.get(idproducto=idproducto)
    data={
        "producto":producto,
    }
    return render(request, "sasg/editarProducto.html", data)

def actualizar_producto(request, idproducto):
    if request.method=='POST':
        producto=Producto.objects.get(idproducto=idproducto)
        
        producto.idproducto=request.POST.get('idproducto')
        producto.fecharegistro=request.POST.get('fecharegistro')
        producto.nomproducto=request.POST.get('nomproducto') 
        producto.nomcategoria=request.POST.get('nomcategoria') 
        producto.cantidad=request.POST.get('cantidad') 
        producto.fechavencimiento=request.POST.get('fechavencimiento') 
        producto.valorlibra=request.POST.get('valorlibra')  
        
        producto.save()
    return redirect("listar_productos")

#--------------------VENTAS----------------------------

def listar_venta(request):
    venta = Venta.objects.all()
    data={
        'venta': venta,
    }
    return render(request, 'sasg/ventas.html',data)

#--------------------PEDIDOS----------------------------

def listar_pedido(request):
    pedido = Pedido.objects.all()
    data={
        'pedido':pedido,
    }
    return render(request, 'sasg/pedidos.html',data)

#--------------------PROVEEDORES----------------------------

def listar_proveedor(request):
    proveedores = Proveedor.objects.all()
    data={
        'proveedores': proveedores,
    }
    return render(request, 'sasg/proveedores.html',data)
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render

<<<<<<< HEAD
from .models import Pedido, Producto, Usuarios, Venta, Roles
=======
from .models import Pedido, Producto, Usuarios, Venta, Proveedor
>>>>>>> 3c539f8a67e9379f9089003b240c8c0a99ec2db8


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

<<<<<<< HEAD
def sasg(request):
    return render(request, 'sasg/index.html')

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

def pre_editar_persona(request,id):
    persona=Persona.objects.get(id=id)
    ciudades=Ciudad.objects.all()
    data={
        "persona":persona,
        "ciudades":ciudades
    }
    return render(request, "personas/editar.html", data)

def actualizar_persona(request, id):
    if request.method=='POST':
        persona=Persona.objects.get(id=id)
        
        persona.documento=request.POST.get('documento')
        persona.nombre=request.POST.get('nombre')
        persona.apellido=request.POST.get('apellido')
        persona.direccion=request.POST.get('direccion')
        persona.correo=request.POST.get('correo')
        persona.ciudad=Ciudad.objects.get(idCiudad=request.POST.get('idCiudad'))
        
        persona.save()
    return redirect("listar_personas")
=======
#proveedores

def proveesView(request):
    proveedores = Proveedor.objects.all()
    data={
        'proveedores': proveedores,
    }
    return render(request, 'sasg/proveedores.html',data)
>>>>>>> 3c539f8a67e9379f9089003b240c8c0a99ec2db8

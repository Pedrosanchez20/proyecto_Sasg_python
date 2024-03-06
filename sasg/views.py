import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password


from .forms import LoginForm
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

def user_login(request):
    
    if request.method == 'POST':  # Si se envió el formulario
        form = LoginForm(request.POST)  # Crea una instancia del formulario con los datos recibidos
        if form.is_valid():  # Verifica si el formulario es válido
            idusuario = form.cleaned_data['idusuario']  # Obtiene el ID de usuario del formulario
            contrasena = form.cleaned_data['contrasena']  # Obtiene la contraseña del formulario
            user = authenticate(request, idusuario=idusuario, contrasena=contrasena)  # Autentica al usuario
            if user is not None and check_password(contrasena, user.contrasena):
                # Autenticación exitosa
                login(request, user)
                return redirect('success_page')
            else:
                # Autenticación fallida
                return render(request, 'sasg/login.html', {'form': form, 'error_message': 'Invalid login'})
    else:
        form = LoginForm()
    return render(request, 'sasg/login.html', {'form': form})


def registrar_usuario(request):
    if request.method == 'POST':
        idusuario = request.POST.get('idusuario')
        idrol = request.POST.get('rol')
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        fechanacimiento = request.POST.get('fechanacimiento')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        contrasena = request.POST.get('contrasena')
        estado = request.POST.get('estado')
        
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

def pre_editar_producto(request,idproducto):
    producto=Producto.objects.get(idproducto=idproducto)
    data={
        "producto":producto,
    }
    return render(request, "sasg/editarProducto.html", data)

def actualizar_producto(request, id):
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
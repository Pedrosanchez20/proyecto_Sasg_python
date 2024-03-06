from cProfile import Profile
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator

from sasg.models import Producto

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
            idproducto=idproducto,
            fecharegistro=fecharegistro,
            nomproducto=nomproducto,
            nomcategoria=nomcategoria,
            cantidad=cantidad,
            fechavencimiento=fechavencimiento,
            valorlibra=valorlibra,
        )
        
        producto.save()
    return redirect("listar_productos")

def listar_producto(request):
    product_list = Producto.objects.all()
    paginator = Paginator(product_list, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sasg/productos.html', {'page_obj': page_obj})

def pre_editar_producto(request,idproducto):
    producto=Producto.objects.get(idproducto=idproducto)
    data={
        "producto":producto,
    }
    return render(request, 'sasg/editarProducto.html',data)

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
    venta_list = Venta.objects.all()
    paginator = Paginator(venta_list, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sasg/ventas.html', {'page_obj': page_obj})

#--------------------PEDIDOS----------------------------

def listar_pedido(request):
    pedido_list = Pedido.objects.all()
    paginator = Paginator(pedido_list, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sasg/pedidos.html', {'page_obj': page_obj})

def pre_editar_pedido(request,idpedido):
    pedido=Pedido.objects.get(idpedido=idpedido)
    usuario=Usuarios.objects.all()
    data={
        "pedido":pedido,
        "usuario":usuario,
    }
    return render(request, 'sasg/editarPedido.html',data)

def actualizar_pedido(request, idpedido):
    if request.method=='POST':
        pedido=Pedido.objects.get(idpedido=idpedido)
        
        pedido.idpedido=request.POST.get('idproducto')
        pedido.fechaemision=request.POST.get('fechaemision')
        pedido.descripcion=request.POST.get('descripcion')
        pedido.estado=request.POST.get('estado')
        pedido.valortotal=request.POST.get('valortotal')    
        pedido.usuario=Usuarios.objects.get(idusuario=request.POST.get('idusuario'))  
          
        
        pedido.save()
    return redirect("listar_pedido")

#--------------------PROVEEDORES----------------------------

def listar_proveedor(request):
    provee_list = Proveedor.objects.all()
    paginator = Paginator(provee_list, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sasg/proveedores.html', {'page_obj': page_obj})
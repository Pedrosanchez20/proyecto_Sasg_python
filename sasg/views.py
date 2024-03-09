import json
from django.urls import reverse
import tempfile
import os

from cProfile import Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from sasg.models import Producto

from .forms import LoginForm
from .models import Compra, Pedido, Producto, Proveedor, Roles, Usuarios, Venta
from .filters import ProductoFilter
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
    if request.method == 'POST':
        idusuario = request.POST.get('idusuario')
        contrasena = request.POST.get('contrasena')
        try:
            usuario = Usuarios.objects.get(idusuario=idusuario)
            if usuario.contrasena == contrasena:
                request.session['user'] = usuario.idusuario
                if usuario.rol.idrol == 971: 
                    return redirect('listar_usuario')  
                elif usuario.rol.idrol == 214:
                    return redirect('listar_productos')  
                elif usuario.rol.idrol == 354:
                    return redirect('index') 
                else:
                    messages.error(request, 'Rol no reconocido.')
            else:
                messages.error(request, 'Contraseña incorrecta.')
        except Usuarios.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')
    return render(request, 'sasg/login.html')


def user_logout(request):
    request.session.flush()
    return redirect('asago')    
            


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
            estado="habilitado",
            rol=Roles.objects.get(idrol=354),
            )
            
        usuario.save()
        mensaje_html = """
        <html>
        <head>
            <style>
                body {
                    font-family: Monaco,monospace;
                    background-color: #737373;
                }
                .container {
                    padding: 20px;
                    background-color: #ffffff;
                    border-radius: 5px;
                    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                }
                h1 {
                    color: red;
                }
                 p {
                    color: #353535 ;
                }

                img{
                    width: 360px
                }
                
                p{
                    font-size: 20px;
                    
                }
                
            </style>
        </head>
        <body>
            <div class="container">
                <h1>¡ASAGO S.A.S TE DA LA BIENVENIDA.!</h1>
                <br>
                <img src="https://lh3.googleusercontent.com/p/AF1QipO5GdPOtKoAywDpXRg9q4sRiM1itwVOxVvwa7s0=w1080-h608-p-no-v0" alt="Derechos reservados">
                <br>
                <p>Esperamos que disfrutes de tu experiencia.</p>
            </div>
        </body>
        </html>
        """
        subject = 'Registro exitoso'
        message = '¡Gracias por registrarte en nuestra pagina!'
        from_email = settings.EMAIL_HOST_USER
        to_email = [email] 
        #send_mail(subject, message, from_email, to_email, html_message=mensaje_html)
        msg = EmailMultiAlternatives(subject, message, from_email, to_email)
        msg.attach_alternative(mensaje_html,"text/html")
        msg.send()
        
        
    return render(request, "sasg/registro.html")


def listar_usuario(request):
    usuario_list = Usuarios.objects.all()
    paginator = Paginator(usuario_list, 13) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sasg/usuarios.html', {'page_obj': page_obj})


def pre_editar_usuario(request, idusuario):
    usuario = Usuarios.objects.get(idusuario=idusuario)
    roles = Roles.objects.all()
    data = {
        "usuarios": usuario,
        "rol": roles,
    }
    return render(request, 'sasg/editarUsuario.html', data)


def actualizar_usuario(request, idusuario):
    if request.method=='POST':
        usuario=Usuarios.objects.get(idusuario=idusuario)
        
        # usuario.idusuario=request.POST.get('idusuario')
        # usuario.nombres=request.POST.get('nombres')
        # usuario.apellidos=request.POST.get('apellidos')
        # usuario.fechanacimiento=request.POST.get('fechanacimiento')
        # usuario.direccion=request.POST.get('direccion')
        # usuario.telefono=request.POST.get('telefono')
        # usuario.email=request.POST.get('email')
        # usuario.contrasena=request.POST.get('contrasena')
        usuario.estado=request.POST.get('estado')
        usuario.rol=Roles.objects.get(idrol=request.POST.get('idrol')) 
        
        usuario.save()
    return redirect("listar_usuario")

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
    return redirect("listar_producto")


def listar_producto(request):
    product_list = Producto.objects.all()
    productoFilter = ProductoFilter(request.GET, queryset=product_list)
    product_list = productoFilter.qs
    paginator = Paginator(product_list, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sasg/productos.html', {'page_obj': page_obj, 'productoFilter': productoFilter})



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

def generarPDF(request):
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Users\Paula\Downloads\wkhtmltox-0.12.6-1.msvc2015-win64.exe")
    pdf = pdfkit.from_url(request.build_absolute_uri(reverse('reportProd')), False, configuration=config)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Productos.pdf'
    return response

def generarCv(request, pk):
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Users\Paula\Downloads\wkhtmltox-0.12.6-1.msvc2015-win64.exe")
    pdf = pdfkit.from_url(request.build_absolute_uri(reverse('specific_user', args=[pk])), False, configuration=config)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Productos.pdf'
    return response

#--------------------VENTAS----------------------------


def listar_venta(request):
    venta_list = Venta.objects.all()
    paginator = Paginator(venta_list, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sasg/ventas.html', {'page_obj': page_obj})

#--------------------COMPRAS----------------------------

def registrar_compra(request):
    if request.method== 'POST':
        idcompra = request.POST.get('idcompra')
        fechaemision = request.POST.get('fechaemision')
        idproveedor = request.POST.get('idproveedor')
        descripcion = request.POST.get('descripcion')
        valorproducto = request.POST.get('valorproducto')
        valortotal = request.POST.get('valortotal')
        
        compra = Compra(
            idcompra = idcompra,
            fechaemision = fechaemision,
            idproveedor = idproveedor,
            descripcion = descripcion,
            valorproducto = valorproducto,
            valortotal = valortotal,
        )
        
        compra.save()
    return redirect("listar_compra")


def listar_compra(request):
    compra_list = Compra.objects.all()
    paginator = Paginator(compra_list, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sasg/compras.html', {'page_obj': page_obj})



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
        
        # pedido.idpedido=request.POST.get('idproducto')
        # pedido.fechaemision=request.POST.get('fechaemision')
        # pedido.descripcion=request.POST.get('descripcion')
        pedido.estado=request.POST.get('estado')
        # pedido.valortotal=request.POST.get('valortotal')    
        # pedido.usuario=Usuarios.objects.get(idusuario=request.POST.get('idusuario'))  
          
        
        pedido.save()
    return redirect("listar_pedido")

#--------------------PROVEEDORES----------------------------


def listar_proveedor(request):
    provee_list = Proveedor.objects.all()
    paginator = Paginator(provee_list, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sasg/proveedores.html', {'page_obj': page_obj})
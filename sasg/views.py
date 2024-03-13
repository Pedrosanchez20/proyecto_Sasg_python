import json
import os
import tempfile
from cProfile import Profile
from random import sample

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.urls import reverse
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from sasg.models import *

from .filters import (CompraFilter, PedidoFilter, ProductoFilter,
                      UsuariosFilter, VentaFilter)

# Create your views here.

def sasg(request):
    return render(request, 'sasg/index.html')

def catcarne(request):
    product_list_carne = Producto.objects.filter(nomcategoria='Carnicos')
    return render(request, 'sasg/catcarne.html', {'product_list_carne': product_list_carne})

def catPollView(request):
    return render(request, 'sasg/catpollo.html')


def catCerdView(request):
    return render(request, 'sasg/catcerdo.html')


def catChoView(request):
    return render(request, 'sasg/catchorizo.html')

def dashboard(request):
    return render(request, 'sasg/dashboard.html')

#--------------------USUARIOS----------------------------

def user_login(request):
    nombre_usuario = None
    if request.method == 'POST':
        idusuario = request.POST.get('idusuario')
        contrasena = request.POST.get('contrasena')
        try:
            usuario = Usuarios.objects.get(idusuario=idusuario)
            if usuario.estado == "habilitado":
                if usuario.contrasena == contrasena:
                    request.session['user'] = usuario.idusuario
                    print("ID del usuario en la sesión:", request.session['user'])
                    nombre_usuario = usuario.nombres
                    print("Nombre de usuario:", nombre_usuario)
                    if usuario.rol.idrol == 971:
                        return redirect('listar_usuario')  
                    elif usuario.rol.idrol == 214:
                        return redirect('listar_productos')  
                    elif usuario.rol.idrol == 354:
                        return redirect('asago') 
                    else:
                        messages.error(request, 'Rol no reconocido.')
                else:
                    messages.error(request, 'Contraseña incorrecta.')
            else:
                messages.error(request, 'El usuario está deshabilitado.') 
        except Usuarios.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')
    return render(request, 'sasg/login.html', {'nombre_usuario': nombre_usuario})




def user_logout(request):
    request.session['user']= None
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
        
        fecha_nacimiento = datetime.strptime(fechanacimiento, '%Y-%m-%d')
        edad_minima = datetime.now() - timedelta(days=365*18)  # 18 años atrás
        if fecha_nacimiento > edad_minima:
            messages.error(request, 'Debes tener al menos 18 años para registrarte.')
            return render(request, "sasg/registro.html", {'error_message': 'Debes tener al menos 18 años para registrarte.'})

        usuario = Usuarios(
            idusuario=idusuario,
            nombres=nombres,
            apellidos=apellidos,
            fechanacimiento=fecha_nacimiento,
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
        message = '¡Gracias por registrarte en nuestra página!'
        from_email = settings.EMAIL_HOST_USER
        to_email = [email] 
        msg = EmailMultiAlternatives(subject, message, from_email, to_email)
        msg.attach_alternative(mensaje_html, "text/html")
        msg.send()

        return redirect('login')
        
    return render(request, "sasg/registro.html")

def listar_usuario(request):
    if request.session['user'] is None:
        return redirect("login")
    else:
        usuario_list = Usuarios.objects.all()
        usuariosFilter = UsuariosFilter(request.GET, queryset=usuario_list)
        usuario_list = usuariosFilter.qs
        paginator = Paginator(usuario_list, 13) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'sasg/usuarios.html', {'page_obj': page_obj, 'usuarioFilter': usuariosFilter})
    
    

def pre_editar_usuario(request, idusuario):
    if request.session['user'] is None:
        return redirect("login")
    else:
        usuario = Usuarios.objects.get(idusuario=idusuario)
        roles = Roles.objects.all()
        data = {
            "usuarios": usuario,
            "rol": roles,
        }
        return render(request, 'sasg/editarUsuario.html', data)

def actualizar_usuario(request, idusuario):
    if request.session['user'] is None:
        return redirect("login")
    else:
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
    

def exportar_usuarios_pdf(request):
    if request.session.get('user') is None:
        return redirect("login")
    else:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="usuarios.pdf"'

        # Obtener la lista de usuarios
        usuario_list = Usuarios.objects.all()

        # Crear un documento PDF
        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        elements = []

        # Agregar título
        titulo = Paragraph('Reporte Usuarios', getSampleStyleSheet()['Heading1'])
        elements.append(titulo)

        elements.append(Spacer(1, 0.5*inch))  # Espacio entre el logo/título y la tabla


        # Definir los datos de los usuarios para la tabla
        data = [['Rol', 'Nombres', 'Apellido', 'Direccion', 'Telefono', 'Email', 'Estado']]
        for usuario in usuario_list:
            data.append([usuario.rol.rolnombre, usuario.nombres, usuario.apellidos,
                         usuario.direccion, usuario.telefono, usuario.email, usuario.estado])

        # Calcular el ancho de las columnas
        col_widths = ['auto'] * len(data[0])  # Todas las columnas tienen ancho automático

        # Crear la tabla y aplicar estilos
        table = Table(data)
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.red),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])
        table.setStyle(style)

        # Añadir la tabla al documento
        elements.append(table)

        # Generar el PDF
        doc.build(elements)
        return response

    
def contar_usuarios(request):
    if request.session['user'] is None:
        return redirect("login")
    else:
        cantidad_usuarios = Usuarios.objects.count()
        return render(request, 'sasg/dashboard.html', {'cantidad_usuarios': cantidad_usuarios})
#--------------------PRODUCTOS----------------------------


def registrar_producto(request):
    if request.session['user'] is None:
        return redirect("login")
    else:
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
                imagen=request.FILES['imagen']
            )
            
            producto.save()
        return redirect("listar_producto")


def listar_producto(request):
    if request.session['user'] is None:
        return redirect("login")
    else:
        product_list = Producto.objects.all()
        productoFilter = ProductoFilter(request.GET, queryset=product_list)
        product_list = productoFilter.qs
        for producto in product_list:
            if int (producto.cantidad) <= 10:
                producto.is_low_quantity = True
            else:
                producto.is_low_quantity = False
        paginator = Paginator(product_list, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'sasg/productos.html', {'page_obj': page_obj, 'productoFilter': productoFilter})


def pre_editar_producto(request,idproducto):
    if request.session['user'] is None:
        return redirect("login")
    else:
        producto=Producto.objects.get(idproducto=idproducto)
        data={
            "producto":producto,
        }
        return render(request, 'sasg/editarProducto.html',data)


def actualizar_producto(request, idproducto):
    if request.session['user'] is None:
        return redirect("login")
    else:
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



def contar_productos(request):
    if request.session['user'] is None:
        return redirect("login")
    else:
        cantidad_producto = Producto.objects.count()
        return render(request, 'sasg/dashboard.html', {'cantidad_productos': cantidad_producto})

   
#-----------------------------------Categorias----------------------------------------

def prod_carne(request):
    product_list_carne = Producto.objects.filter(nomcategoria='carne')
    return render(request, 'sasg/catcarne.html', {'product_list_carne': product_list_carne})

def prod_pollo(request):
    product_list_pollo = Producto.objects.filter(nomcategoria='pollo')
    return render(request, 'sasg/catpollo.html', {'product_list_pollo': product_list_pollo})

def prod_cerdo(request):
    product_list_cerdo = Producto.objects.filter(nomcategoria='cerdo')
    return render(request, 'sasg/catcerdo.html', {'product_list_cerdo': product_list_cerdo})

def prod_chorizo(request):
    product_list_chorizo = Producto.objects.filter(nomcategoria='chorizo')
    return render(request, 'sasg/catchorizo.html', {'product_list_chorizo': product_list_chorizo})
#--------------------VENTAS----------------------------


def listar_venta(request):
    if request.session['user'] is None:
        return redirect("login")
    else:
        venta_list = Venta.objects.all()
        ventaFilter = VentaFilter(request.GET, queryset=venta_list)
        venta_list = ventaFilter.qs
        paginator = Paginator(venta_list, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'sasg/ventas.html', {'page_obj': page_obj, 'ventaFilter': ventaFilter})

#--------------------COMPRAS----------------------------

def registrar_compra(request):
    if request.session['user'] is None:
        return redirect("login")
    else:
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
    if request.session['user'] is None:
        return redirect("login")
    else:
        compra_list = Compra.objects.all()
        compraFilter = CompraFilter(request.GET, queryset=compra_list)
        compra_list = compraFilter.qs
        paginator = Paginator(compra_list, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'sasg/compras.html', {'page_obj': page_obj, 'compraFilter':compraFilter})



#--------------------PEDIDOS----------------------------


def listar_pedido(request):
    if request.session['user'] is None:
        return redirect("login")
    else:
        pedido_list = Pedido.objects.all()
        pedidoFilter = PedidoFilter(request.GET, queryset=pedido_list)
        pedido_list = pedidoFilter.qs
        paginator = Paginator(pedido_list, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'sasg/pedidos.html', {'page_obj': page_obj, 'pedidoFilter':pedidoFilter})


def pre_editar_pedido(request,idpedido):
    if request.session['user'] is None:
        return redirect("login")
    else:
        pedido=Pedido.objects.get(idpedido=idpedido)
        usuario=Usuarios.objects.all()
        data={
            "pedido":pedido,
            "usuario":usuario,
        }
        return render(request, 'sasg/editarPedido.html',data)


def actualizar_pedido(request, idpedido):
    if request.session['user'] is None:
        return redirect("login")
    else:
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
    if request.session['user'] is None:
        return redirect("login")
    else:
        provee_list = Proveedor.objects.all()
        paginator = Paginator(provee_list, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'sasg/proveedores.html', {'page_obj': page_obj})
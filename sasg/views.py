import json
import os
import random
import tempfile
from cProfile import Profile
from datetime import datetime, timedelta
from random import sample
from django.contrib.auth.decorators import login_required

from django.db.models import Count
import plotly.graph_objs as go

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.db import transaction
from datetime import date
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.forms import formset_factory
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (Image, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)

from sasg.models import *

from .filters import (CompraFilter, PedidoFilter, ProductoFilter,
                      UsuariosFilter, VentaFilter, ProveedorFilter)
from .forms import CompraForm, VentaForm, DetalleVentaForm

def validarSesion(request):
    if request.session.get('usuario_logeado') is None:
        return True
    return False

def recuperarSesion(request):
    return Usuarios.objects.get(idusuario=request.session.get('usuario_logeado'))

def sasg(request):
    if validarSesion(request):
        return render(request, 'sasg/index.html')
    else:
        usuario = Usuarios.objects.get(idusuario=request.session.get('usuario_logeado'))
        return render(request, 'sasg/index.html', {'usuario': usuario})

def dashboard(request):
    data = {
        'cantidad_usuarios' : Usuarios.objects.count(),
        'cantidad_producto' : Producto.objects.count(),
        'cantidad_venta' : Venta.objects.count(),
        'cantidad_pedido' : Pedido.objects.count(),
        'cantidad_compra' : Compra.objects.count(),
        'usuario': recuperarSesion(request),
        
    }
    try:
        if validarSesion(request):
            return redirect("login")
        elif validar_rol(request) == 1:
            return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)})
        elif validar_rol(request) == 2:
            return render(request, 'sasg/dashboard.html' , data)  
        elif validar_rol(request) == 3:
            return render(request, 'sasg/dashboard.html' , data)  
    except Exception:
        return redirect('login')
    
    
def graficos(request):
    cantidad_usuarios = Usuarios.objects.count()  
    ventas_por_mes = [venta.cantidad for venta in Venta.objects.all()]  
    return render(request, 'sasg/graficos.html', {'cantidad_usuarios': cantidad_usuarios, 'ventas_por_mes': ventas_por_mes})

#-----------------------------------------USUARIOS-------------------------------------

def user_login(request):
    if request.method == 'POST':
        idusuario = request.POST.get('idusuario')
        contrasena = request.POST.get('contrasena')
        try:
            usuario = Usuarios.objects.get(idusuario=idusuario)
            if usuario.estado == "habilitado" and check_password(contrasena, usuario.contrasena):
                request.session['usuario_logeado'] = usuario.idusuario
                
                if usuario.rol.idrol in [971, 214]:
                    # messages.success(request, f'Bienvenido a asago {usuario.nombres}')
                    return redirect('dashboard')
                                    
                elif usuario.rol.idrol == 354:
                    # messages.success(request, f'Bienvenido a asago {usuario.nombres}')
                    return redirect('asago')
                else:
                    messages.error(request, 'Rol no reconocido.')
                    return render(request, 'sasg/login.html', {})
                
            elif usuario.estado != "habilitado":
                messages.error(request, 'El usuario está deshabilitado.')
            else:
                messages.error(request, 'Usuario no encontrado o contraseña incorrecta.')
        except Usuarios.DoesNotExist:
            messages.error(request, 'Usuario no encontrado o contraseña incorrecta.')
        except Exception as e:
            messages.error(request, 'Error interno al procesar el inicio de sesión.')
            
    return render(request, 'sasg/login.html', {})

def validar_rol(request):
    usuario = Usuarios.objects.get(idusuario = request.session.get('usuario_logeado'))
    if usuario.rol.idrol == 354:
        return 1
    elif usuario.rol.idrol == 214:
        return 2
    elif usuario.rol.idrol == 971:
        return 3
    return False

def logout(request):
    if 'carrito_productos' in request.session:
        del request.session['carrito_productos']  
    if 'usuario_logeado' in request.session:
        del request.session['usuario_logeado'] 
    return redirect('asago')

def user_logout(request):
    if 'carrito_productos' in request.session:
        del request.session['carrito_productos']
        
    if 'usuario_logeado' in request.session:
        del request.session['usuario_logeado']
            
    return redirect('asago')
     
def recuperar_contrasena(request):
    if request.method == 'POST':
        correo = request.POST.get('email')
        usuario = Usuarios.objects.get(email = correo)
        codigo = random.randint(1000, 9999)
        contrasena_encriptada = make_password(str(codigo))
        usuario.contrasena = contrasena_encriptada
        usuario.save()
        subject = 'Recuperar Contraseña'
        message = str(codigo)
        from_email = settings.EMAIL_HOST_USER
        to_email = [correo] 
        msg = EmailMultiAlternatives(subject, message, from_email, to_email)
        msg.send()
        return redirect('login')
    return render(request,"sasg/recuperarcontrasena.html")
    

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
        contrasena_encriptada = make_password(contrasena)
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
            contrasena=contrasena_encriptada,
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
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
         return render(request, 'sasg/index.html', {})
    elif validar_rol(request) == 2:
        return render(request, 'sasg/dashboard.html' ,{'usuario': recuperarSesion(request)}) 
    else:
        usuario_list = Usuarios.objects.all()
        usuariosFilter = UsuariosFilter(request.GET, queryset=usuario_list)
        usuario_list = usuariosFilter.qs
        paginator = Paginator(usuario_list, 13)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'sasg/usuarios.html', {'page_obj': page_obj, 'usuarioFilter': usuariosFilter, 'usuario': recuperarSesion(request)})
    
    
def pre_editar_usuario(request, idusuario):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
         return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)})
    elif validar_rol(request) == 2:
        return render(request, 'sasg/dashboard.html' ,{'usuario': recuperarSesion(request)}) 
    else:
        usuario = Usuarios.objects.get(idusuario=idusuario)
        roles = Roles.objects.all()
        data = {
            "usuarios": usuario,
            "rol": roles,
        }
        return render(request, 'sasg/editarUsuario.html', data)

def actualizar_usuario(request, idusuario):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
         return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)})
    elif validar_rol(request) == 2:
        return render(request, 'sasg/dashboard.html' ,{'usuario': recuperarSesion(request)}) 
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
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
         return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)})
    elif validar_rol(request) == 2:
        return render(request, 'sasg/dashboard.html' ,{'usuario': recuperarSesion(request)}) 
    else:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="usuarios.pdf"'

        usuario_list = Usuarios.objects.all()

        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        elements = []

        titulo = Paragraph('Reporte Usuarios', getSampleStyleSheet()['Heading1'])
        elements.append(titulo)

        elements.append(Spacer(1, 0.5*inch))

        data = [['Rol', 'Nombres', 'Apellido', 'Direccion', 'Telefono', 'Email', 'Estado']]
        for usuario in usuario_list:
            data.append([usuario.rol.rolnombre, usuario.nombres, usuario.apellidos,
                         usuario.direccion, usuario.telefono, usuario.email, usuario.estado])

        col_widths = ['auto'] * len(data[0]) 

        table = Table(data)
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.red),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])
        table.setStyle(style)

        elements.append(table)

        doc.build(elements)
        return response

    
#-----------------------------------------PRODUCTOS------------------------------------

def registrar_producto(request):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
         return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)})
    else:
        if request.method== 'POST':
            idproducto=request.POST.get('idproducto')
            fecharegistro = timezone.now().date()
            nomproducto=request.POST.get('nomproducto')
            nomcategoria=request.POST.get('nomcategoria')
            fechavencimiento=request.POST.get('fechavencimiento')
            valorlibra=request.POST.get('valorlibra')
            
            producto = Producto(
                idproducto=idproducto,
                fecharegistro=fecharegistro,
                nomproducto=nomproducto,
                nomcategoria=nomcategoria,
                cantidad=0,
                fechavencimiento=fechavencimiento,
                valorlibra=valorlibra,
                imagen=request.FILES['imagen']
            )
            
            producto.save()
        return redirect("listar_producto")


def listar_producto(request):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
         return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)})
    else:
        product_list = Producto.objects.all()
        productoFilter = ProductoFilter(request.GET, queryset=product_list)
        product_list_filtered = productoFilter.qs
        for producto in product_list_filtered:
            if producto.cantidad: 
                producto.is_low_quantity = int(producto.cantidad) <= 10
            else:
                producto.is_low_quantity = False
        fecha_actual = datetime.now().date()

        dias_proximo_vencimiento = 7
        productos_proximos_vencer = []
        for producto in product_list:
            if producto.fechavencimiento:
                dias_restantes = (producto.fechavencimiento - fecha_actual).days
                producto.is_proximo_vencimiento = dias_restantes <= dias_proximo_vencimiento
                if producto.is_proximo_vencimiento:
                    productos_proximos_vencer.append(producto)  
        paginator = Paginator(product_list_filtered, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'sasg/productos.html', {'page_obj': page_obj, 'productoFilter': productoFilter, 'productos_proximos_vencer': productos_proximos_vencer, 'usuario':recuperarSesion(request)})


def pre_editar_producto(request,idproducto):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
         return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)})
    elif validar_rol(request) == 2:
        return render(request, 'sasg/dashboard.html' ,{'usuario': recuperarSesion(request)}) 
    else:
        producto=Producto.objects.get(idproducto=idproducto)
        data={
            "producto":producto,
        }
        return render(request, 'sasg/editarProducto.html',data)


def actualizar_producto(request, idproducto):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
         return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)})
    elif validar_rol(request) == 2:
        return render(request, 'sasg/dashboard.html' ,{'usuario': recuperarSesion(request)}) 
    else:
        if request.method=='POST':
            producto=Producto.objects.get(idproducto=idproducto)
            
            producto.idproducto=request.POST.get('idproducto')
            producto.fecharegistro = Producto.objects.get(idproducto=idproducto).fecharegistro
            producto.nomproducto=request.POST.get('nomproducto')
            producto.nomcategoria=request.POST.get('nomcategoria')
            producto.fechavencimiento=request.POST.get('fechavencimiento')
            producto.valorlibra=request.POST.get('valorlibra')
            producto.imagen = request.FILES['imagen'] if 'imagen' in request.FILES else producto.imagen
            
            producto.save()
        return redirect("listar_producto")

def exportar_productos_pdf(request):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
         return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)})
    elif validar_rol(request) == 2:
        return render(request, 'sasg/dashboard.html' ,{'usuario': recuperarSesion(request)}) 
    else:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="productos.pdf"'

        producto_list = Producto.objects.all()

        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        elements = []

        titulo = Paragraph('Reporte Productos', getSampleStyleSheet()['Heading1'])
        elements.append(titulo)

        elements.append(Spacer(1, 0.5*inch))  


        data = [['ID', 'Fecha Registro', 'Nombre', 'Categoria', 'Cantidad', 'Fecha Vencimiento', 'Valor Libra']]
        for producto in producto_list:
            data.append([producto.idproducto, producto.fecharegistro, producto.nomproducto,
                         producto.nomcategoria, producto.cantidad, producto.fechavencimiento, producto.valorlibra])

        col_widths = ['auto'] * len(data[0]) 

        table = Table(data)
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.red),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])
        table.setStyle(style)

        elements.append(table)

        doc.build(elements)
        return response


def contar_productos(request):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
         return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)})
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

#--------------------------------------------VENTAS--------------------------------------

@transaction.atomic
def registrar_venta(request):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
         return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)})
    else:
        if request.method == 'POST':
            form = VentaForm(request.POST)
            if form.is_valid():
                total_valor = 0
                productos_invalidos = []
                venta = form.save(commit=False)
                venta.fechaemision = timezone.localtime(timezone.now())
                venta.save()  
                for producto in form.cleaned_data['productos']:
                    cantidad = form.cleaned_data['cantidad_producto_{}'.format(producto.idproducto)]
                    if cantidad > 0 and producto.cantidad >= cantidad:
                        detalle = Detalleventa.objects.create(
                            idventa=venta,
                            idproducto=producto,
                            cantidad=cantidad,
                            valorproducto=producto.valorlibra
                        )
                        detalle.save()
                        total_valor += detalle.valorproducto * cantidad
                        producto.cantidad -= cantidad
                        producto.save()
                    else:
                        productos_invalidos.append(producto)
                if productos_invalidos:
                    for producto_invalido in productos_invalidos:
                        form.add_error(None, f"No hay suficientes unidades disponibles de {producto_invalido.nomproducto}")
                    return render(request, 'sasg/registrar_venta.html', {'form': form})
                venta.valortotal = total_valor
                venta.save() 
                return redirect('listar_venta')
        else:
            form = VentaForm()
            form.fields['productos'].queryset = Producto.objects.all()
        return render(request, 'sasg/registrar_venta.html', {'form': form})


def listar_venta(request):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
         return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)})
    else:
        productos_mas_vendidos = Detalleventa.objects.values('idproducto__nomproducto').annotate(total_vendido=Count('idproducto')).order_by('-total_vendido')[:10]
        productos = [item['idproducto__nomproducto'] for item in productos_mas_vendidos]
        cantidades = [item['total_vendido'] for item in productos_mas_vendidos]
        grafico = go.Figure(data=[go.Pie(labels=productos, values=cantidades)])
        grafico.update_traces(marker=dict(colors=['#add8e6', '#87cefa', '#00bfff', '#1e90ff', '#6495ed', '#4169e1', '#0000ff', '#0000cd', '#00008b', '#000080'], line=dict(color='#FFFFFF', width=1.5)))
        grafico.update_layout(title='Productos más Vendidos', title_x=0.5)
        grafico_html = grafico.to_html(full_html=False, default_height=500, default_width=700)
        venta_list = Venta.objects.all()
        ventaFilter = VentaFilter(request.GET, queryset=venta_list)
        venta_list = ventaFilter.qs
        paginator = Paginator(venta_list, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'sasg/ventas.html', {'page_obj': page_obj, 'ventaFilter': ventaFilter, 'usuario':recuperarSesion(request), 'grafico_html': grafico_html})
    

def exportar_ventas_pdf(request):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
         return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)})
    elif validar_rol(request) == 2:
        return render(request, 'sasg/dashboard.html' ,{'usuario': recuperarSesion(request)}) 
    else:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="ventas.pdf"'

        venta_list = Venta.objects.all()

        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        elements = []

        titulo = Paragraph('Reporte Ventas', getSampleStyleSheet()['Heading1'])
        elements.append(titulo)

        elements.append(Spacer(1, 0.5*inch))  


        data = [['ID', 'Fecha Emision', 'Valor Total']]
        for venta in venta_list:
            data.append([venta.idventa, venta.fechaemision, venta.valortotal])

        col_widths = ['auto'] * len(data[0]) 

        table = Table(data)
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.red),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])
        table.setStyle(style)

        elements.append(table)

        doc.build(elements)
        return response

def detalle_venta(request, venta_id):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
         return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)})
    elif validar_rol(request) == 2:
        return render(request, 'sasg/dashboard.html' ,{'usuario': recuperarSesion(request)}) 
    else:
        venta = get_object_or_404(Venta, idventa=venta_id)
        detalles = venta.obtener_detalles()
        return render(request, 'sasg/detalle_venta.html', {'venta': venta, 'detalles': detalles})

#------------------------COMPRAS------------------------------

@transaction.atomic
def registrar_compra(request):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
         return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)})
    elif validar_rol(request) == 2:
        return render(request, 'sasg/dashboard.html' ,{'usuario': recuperarSesion(request)}) 
    else:
        if request.method == 'POST':
            form = CompraForm(request.POST)
            if form.is_valid():
                compra = form.save(commit=False)
                total_valor = 0
                compra.fechaemision = timezone.localtime(timezone.now())
                compra.save() 
                for producto in form.cleaned_data['productos']:
                    cantidad = form.cleaned_data['cantidad_producto_{}'.format(producto.idproducto)]
                    if cantidad > 0:
                        detalle = DetalleCompra.objects.create(
                            idcompra=compra,
                            idproducto=producto,
                            cantidad=cantidad,
                            valorproducto=producto.valorlibra
                        )
                        detalle.save()
                        total_valor += detalle.valorproducto * cantidad
                        producto.cantidad += cantidad
                        producto.save()
                compra.valortotal = total_valor
                compra.save()  # Actualiza la compra con el valor total
                return redirect('listar_compra')
        else:
            form = CompraForm()
            form.fields['productos'].queryset = Producto.objects.all()
        return render(request, 'sasg/registrar_compra.html', {'form': form})


def listar_compra(request):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
         return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)})
    elif validar_rol(request) == 2:
        return render(request, 'sasg/dashboard.html' ,{'usuario': recuperarSesion(request)}) 
    else:
        compra_list = Compra.objects.all()
        compraFilter = CompraFilter(request.GET, queryset=compra_list)
        compra_list = compraFilter.qs
        paginator = Paginator(compra_list, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'sasg/compras.html', {'page_obj': page_obj, 'compraFilter':compraFilter, 'usuario':recuperarSesion(request)})
    
    
def exportar_compras_pdf(request):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
         return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)})
    elif validar_rol(request) == 2:
        return render(request, 'sasg/dashboard.html' ,{'usuario': recuperarSesion(request)}) 
    else:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="compras.pdf"'

        compra_list = Compra.objects.all()

        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        elements = []

        titulo = Paragraph('Reporte Compras', getSampleStyleSheet()['Heading1'])
        elements.append(titulo)

        elements.append(Spacer(1, 0.5*inch))  


        data = [['ID', 'Fecha Emision', 'Proveedor', 'Descripcion', 'Valor Total']]
        for compra in compra_list:
            data.append([compra.idcompra, compra.fechaemision, compra.idproveedor.nomempresa,
                         compra.descripcion, compra.valortotal])

        col_widths = ['auto'] * len(data[0]) 

        table = Table(data)
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.red),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])
        table.setStyle(style)

        elements.append(table)

        doc.build(elements)
        return response

def detalle_compra(request, compra_id):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
         return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)})
    elif validar_rol(request) == 2:
        return render(request, 'sasg/dashboard.html' ,{'usuario': recuperarSesion(request)}) 
    else:
        compra = get_object_or_404(Compra, idcompra=compra_id)
        detalles = compra.obtener_detalles()
        return render(request, 'sasg/detalle_compra.html', {'compra': compra, 'detalles': detalles})

#-------------------------------PEDIDOS-------------------------------------

def listar_pedido(request):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
        return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)})
    else:
        pedido_list = Pedido.objects.all()
        pedidoFilter = PedidoFilter(request.GET, queryset=pedido_list)
        pedido_list = pedidoFilter.qs
        paginator = Paginator(pedido_list, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'sasg/pedidos.html', {'page_obj': page_obj, 'pedidoFilter': pedidoFilter, 'usuario': recuperarSesion(request)})

def pre_editar_pedido(request,idpedido):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
         return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)}) 
    else:
        pedido=Pedido.objects.get(idpedido=idpedido)
        usuario=Usuarios.objects.all()
        data={
            "pedido":pedido,
            "usuario":usuario,
        }
        return render(request, 'sasg/editarPedido.html',data)

def actualizar_pedido(request, idpedido):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
         return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)})
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
    
def exportar_pedidos_pdf(request):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
         return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)})
    elif validar_rol(request) == 2:
        return render(request, 'sasg/dashboard.html' ,{'usuario': recuperarSesion(request)}) 
    else:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="pedidos.pdf"'

        pedido_list = Pedido.objects.all()

        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        elements = []

        titulo = Paragraph('Reporte Pedidos', getSampleStyleSheet()['Heading1'])
        elements.append(titulo)

        elements.append(Spacer(1, 0.5*inch))  


        data = [['ID', 'Usuario', 'Fecha Emision', 'Estado', 'Valor Total']]
        for pedido in pedido_list:
            data.append([pedido.idpedido, pedido.idusuario , pedido.fechacreacion,
                          pedido.estado, pedido.totalpedido])

        col_widths = ['auto'] * len(data[0]) 

        table = Table(data)
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.red),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])
        table.setStyle(style)

        elements.append(table)

        doc.build(elements)
        return response

def carrito(request):
    carrito = request.session.get('carrito_productos', {})
    productos_carrito = []
    total = 0
    for producto_id, item in carrito.items():
        producto = get_object_or_404(Producto, idproducto=producto_id)
        producto_info = {
            'id': producto_id,
            'nombre': item['nombre'],
            'precio': item['precio'],
            'imagen': item['imagen'],
            'cantidad': item.get('cantidad', 1)
        }
        productos_carrito.append(producto_info)
        total += item['precio'] * producto_info['cantidad']
    context = {'productos_carrito': productos_carrito, 'total': total}
    return render(request, 'sasg/carrito.html', context)

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, idproducto=producto_id)
    if producto:
        carrito = request.session.get('carrito_productos', {})
        if producto_id in carrito:
            pass
        else:
            carrito[producto_id] = {
                'nombre': producto.nomproducto,
                'cantidad': 1,
                'precio': producto.valorlibra,
                'imagen': producto.imagen.url,
                'usuario_id': request.session.get('usuario_logeado')
            }
            request.session['carrito_productos'] = carrito
    else:
        messages.error(request, "El producto seleccionado no existe.")
        
    return redirect('asago')

def actualizar_cantidad_carrito(request, producto_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        producto_id = request.POST.get('producto_id')
        if action in ['sumar', 'restar']:
            carrito = request.session.get('carrito_productos', {})
            if producto_id in carrito:
                if action == 'sumar':
                    carrito[producto_id]['cantidad'] += 1
                elif action == 'restar':
                    if carrito[producto_id]['cantidad'] > 1:
                        carrito[producto_id]['cantidad'] -= 1
                request.session['carrito_productos'] = carrito
    return redirect('carrito')

def eliminar_producto_carrito(request, producto_id):
    if request.method == 'POST':
        if 'carrito_productos' in request.session:
            carrito = request.session['carrito_productos']
            if str(producto_id) in carrito:
                del carrito[str(producto_id)]
                request.session['carrito_productos'] = carrito
    return redirect('carrito')

def eliminar_todo_carrito(request):
    if request.method == 'POST':
        if 'carrito_productos' in request.session:
            del request.session['carrito_productos']
            messages.success(request, "Se han eliminado todos los productos del carrito.")
    return redirect('carrito')

@transaction.atomic
def hacer_pedido(request):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 2:
        return render(request, 'sasg/dashboard.html' ,{'usuario': recuperarSesion(request)}) 
    else:
        if request.method == 'POST':
            carrito = request.session.get('carrito_productos', {})
            if carrito:
                usuario_id = carrito.get(next(iter(carrito)),'').get('usuario_id')
                usuario = Usuarios.objects.get(idusuario=usuario_id) if usuario_id else None 

                nuevo_pedido = Pedido.objects.create(
                    idusuario=usuario,
                    estado='En espera',
                    fechacreacion=datetime.now(),
                    totalpedido=sum(item['precio'] * item['cantidad'] for item in carrito.values())
                )

                for producto_id, item in carrito.items():
                    producto = get_object_or_404(Producto, idproducto=producto_id)
                    cantidad_carrito = item['cantidad']
                    producto.cantidad -= cantidad_carrito
                    producto.save()
                    
                    DetallePedido.objects.create(
                        idpedido=nuevo_pedido,
                        idproducto=producto,
                        cantidad=cantidad_carrito,
                        valorproducto=item['precio']
                    )
                del request.session['carrito_productos']
                return redirect('carrito')
            else:
                messages.error(request, "No hay productos en el carrito.")
        return redirect('carrito')

def pedidos_cliente(request):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 2:
        return render(request, 'sasg/dashboard.html' ,{'usuario': recuperarSesion(request)}) 
    else:
        if request.session.get('usuario_logeado') is None:
            return redirect('login')
        
        usuario_logeado_id = request.session.get('usuario_logeado')
        
        pedidos_usuario = Pedido.objects.filter(idusuario_id=usuario_logeado_id).order_by('-fechacreacion')
        paginator = Paginator(pedidos_usuario, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'sasg/pedidos_cliente.html', {'page_obj': page_obj,'pedidos_usuario': pedidos_usuario, 'usuario':recuperarSesion(request)})

def detalle_pedido(request, pedido_id):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 2:
        return render(request, 'sasg/dashboard.html' ,{'usuario': recuperarSesion(request)}) 
    else:
        detalles_pedido = DetallePedido.objects.filter(idpedido=pedido_id)
        return render(request, 'sasg/detalle_pedido.html', {'detalles_pedido': detalles_pedido})

#--------------------PROVEEDORES----------------------------

def listar_proveedor(request):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
         return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)})
    elif validar_rol(request) == 2:
        return render(request, 'sasg/dashboard.html' ,{'usuario': recuperarSesion(request)}) 
    else:
        usuario = Usuarios.objects.get(idusuario=request.session.get('usuario_logeado'))
        provee_list = Proveedor.objects.all()
        proveedorFilter = ProveedorFilter(request.GET, queryset=provee_list)
        provee_list = proveedorFilter.qs
        paginator = Paginator(provee_list, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'sasg/proveedores.html', {'page_obj': page_obj, 'provee_list': provee_list ,'usuario':usuario, 'proveedorFilter': proveedorFilter})
    
def registrar_proveedor(request):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
         return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)})
    elif validar_rol(request) == 2:
        return render(request, 'sasg/dashboard.html' ,{'usuario': recuperarSesion(request)}) 
    else:
        if request.method== 'POST':
            idproveedor = request.POST.get('idproveedor')
            nomempresa = request.POST.get('nomempresa')
            telefono = request.POST.get('telefono')
            correo = request.POST.get('correo')

            proveedor = Proveedor(
                idproveedor = idproveedor,
                nomempresa = nomempresa,
                telefono = telefono,
                correo = correo,
            )

            proveedor.save()
        return redirect("listar_proveedor")    


def pre_editar_proveedor(request,idproveedor):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
         return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)})
    elif validar_rol(request) == 2:
        return render(request, 'sasg/dashboard.html' ,{'usuario': recuperarSesion(request)}) 
    else:
        proveedor=Proveedor.objects.get(idproveedor=idproveedor)
        usuario=Usuarios.objects.all()
        data={
            "proveedor":proveedor,
            "usuario":usuario,
        }
        return render(request, 'sasg/editarProveedor.html',data)


def actualizar_proveedor(request, idproveedor):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
         return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)})
    elif validar_rol(request) == 2:
        return render(request, 'sasg/dashboard.html' ,{'usuario': recuperarSesion(request)}) 
    else:
        if request.method=='POST':
            proveedor=Proveedor.objects.get(idproveedor=idproveedor)

            # proveedor.idproveedor=request.POST.get('idproveedor')
            proveedor.nomempresa=request.POST.get('nomempresa')
            proveedor.producto=request.POST.get('producto')
            proveedor.telefono=request.POST.get('telefono')   
            proveedor.correo=request.POST.get('correo')  
            # pedido.usuario=Usuarios.objects.get(idusuario=request.POST.get('idusuario'))  


            proveedor.save()
        return redirect("listar_proveedor")
    
    
def exportar_proveedores_pdf(request):
    if validarSesion(request):
        return redirect("login")
    elif validar_rol(request) == 1:
         return render(request, 'sasg/index.html', {'usuario': recuperarSesion(request)})
    elif validar_rol(request) == 2:
        return render(request, 'sasg/dashboard.html' ,{'usuario': recuperarSesion(request)}) 
    else:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="proveedores.pdf"'

        proveedor_list = Proveedor.objects.all()

        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        elements = []

        titulo = Paragraph('Reporte Proveedores', getSampleStyleSheet()['Heading1'])
        elements.append(titulo)

        elements.append(Spacer(1, 0.5*inch))  


        data = [['ID', 'Empresa', 'Telefono', 'Correo']]
        for proveedor in proveedor_list:
            data.append([proveedor.idproveedor, proveedor.nomempresa ,
                          proveedor.telefono, proveedor.correo])

        col_widths = ['auto'] * len(data[0]) 

        table = Table(data)
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.red),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])
        table.setStyle(style)

        elements.append(table)

        doc.build(elements)
        return response
    
    
#--------------------ERROR404----------------------------
def pagina_no_encontrada(request, exception):
    return render(request, 'sasg/error404.html', status=404)
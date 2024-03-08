from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('',views.sasg,name='asago'),
    path('catPollo',views.catPollView,name='catPollo'),
    path('catCarne',views.catCarnView,name='catCarne'),
    path('catCerdo',views.catCerdView,name='catCerdo'),
    path('catChorizo',views.catChoView,name='catChorizo'),
    
    #/-----usuarios------/
    path('listar_usuario/',login_required(views.listar_usuario), name='listar_usuario'),
    path('registrar_usuario/',views.registrar_usuario,name='registrar_usuario'),
    path('pre_editar_usuario/<str:idusuario>',login_required(views.pre_editar_usuario),name='pre_editar_usuario'),
    path('actualizar_usuario/<str:idusuario>/', login_required(views.actualizar_usuario), name='actualizar_usuario'),
    
    #/-----productos------/
    path('listar_productos/',login_required(views.listar_producto),name='listar_productos'),
    path('registrar_producto/',login_required(views.registrar_producto),name='registrar_producto'),
    path('pre_editar_producto/<str:idproducto>',login_required(views.pre_editar_producto),name='pre_editar_producto'),
    path('actualizar_producto/<str:idproducto>',login_required(views.actualizar_producto),name='actualizar_producto'),
    path('generarPDF/',views.generarPDF,name='generarPDF'),
    path('generarCv/<int:pk>',views.generarCv,name='generarCv'),

    #/-----ventas------/
    path('listar_venta/',login_required(views.listar_venta),name='listar_venta'),
    
    #/-----Compras----/
    path('listar_compra/',login_required(views.listar_compra),name='listar_compra'),
     path('registrar_compra/',login_required(views.registrar_compra),name='registrar_compra'),
     
    #/-----pedidos------/
    path('listar_pedido/',login_required(views.listar_pedido),name='listar_pedido'),
    path('pre_editar_pedido/<str:idpedido>',login_required(views.pre_editar_pedido),name='pre_editar_pedido'),
    path('actualizar_pedido/<str:idpedido>',login_required(views.actualizar_pedido),name='actualizar_pedido'),
    
    #/-----proveedores------/
    path('listar_proveedor/',login_required(views.listar_proveedor),name='listar_proveedor'),
    path('listar_proveedor/',login_required(views.listar_proveedor),name='listar_proveedor'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout, name='logout'),
]

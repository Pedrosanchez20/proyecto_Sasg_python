from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from . import views

#from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('',views.sasg,name='asago'),
    path('catPollo',views.catPollView,name='catPollo'),
    path('catcarne',views.catcarne,name='catcarne'),
    path('catCerdo',views.catCerdView,name='catCerdo'),
    path('catChorizo',views.catChoView,name='catChorizo'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('contar_productos',views.contar_productos,name='contar_productos'),
    path('contar_usuarios',views.contar_usuarios,name='contar_usuarios'),
    #/-----usuarios------/
    path('listar_usuario/',views.listar_usuario,name='listar_usuario'),
    path('registrar_usuario/',views.registrar_usuario,name='registrar_usuario'),
    path('pre_editar_usuario/<str:idusuario>',views.pre_editar_usuario,name='pre_editar_usuario'),
    path('actualizar_usuario/<str:idusuario>/', views.actualizar_usuario,name='actualizar_usuario'),
    
    #/-----productos------/
    path('listar_producto/',views.listar_producto,name='listar_producto'),
    path('registrar_producto/',views.registrar_producto,name='registrar_producto'),
    path('pre_editar_producto/<str:idproducto>',views.pre_editar_producto,name='pre_editar_producto'),
    path('actualizar_producto/<str:idproducto>',views.actualizar_producto,name='actualizar_producto'),
    #/-----ventas------/
    path('listar_venta/',views.listar_venta,name='listar_venta'),
    
    #/-----Compras----/
    path('listar_compra/',views.listar_compra,name='listar_compra'),
    path('registrar_compra/',views.registrar_compra,name='registrar_compra'),
     
    #/-----pedidos------/
    path('listar_pedido/',views.listar_pedido,name='listar_pedido'),
    path('pre_editar_pedido/<str:idpedido>',views.pre_editar_pedido,name='pre_editar_pedido'),
    path('actualizar_pedido/<str:idpedido>',views.actualizar_pedido,name='actualizar_pedido'),
    
    #/-----proveedores------/
    path('listar_proveedor/',views.listar_proveedor,name='listar_proveedor'),
    path('registrar_proveedor/',views.registrar_proveedor,name='registrar_proveedor'),
    path('pre_editar_proveedor/<str:idproveedor>',views.pre_editar_proveedor,name='pre_editar_proveedor'),
    path('actualizar_proveedor/<str:idproveedor>',views.actualizar_proveedor,name='actualizar_proveedor'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout, name='logout'),
    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

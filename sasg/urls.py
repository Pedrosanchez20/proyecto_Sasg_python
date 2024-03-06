from django.urls import path

from . import views

urlpatterns = [
    path('',views.sasg,name='asago'),
    path('catPollo',views.catPollView,name='catPollo'),
    path('catCarne',views.catCarnView,name='catCarne'),
    path('catCerdo',views.catCerdView,name='catCerdo'),
    path('catChorizo',views.catChoView,name='catChorizo'),
    #/-----usuarios------/
    path('listar_usuario/',views.listar_usuario, name='listar_usuario'),
    #/-----productos------/
    path('listar_productos/',views.listar_producto,name='listar_productos'),
    path('pre_editar_producto/<str:idproducto>',views.pre_editar_producto,name='pre_editar_producto'),
    path('actualizar_producto/<str:idproducto>',views.actualizar_producto,name='actualizar_producto'),
    path('registrar_producto/',views.registrar_producto,name='registrar_producto'),
    #/-----ventas------/
    path('listar_venta/',views.listar_venta,name='listar_venta'),
    #/-----pedidos------/
    path('listar_pedido/',views.listar_pedido,name='listar_pedido'),
    #/-----proveedores------/
    path('listar_proveedor/',views.listar_proveedor,name='listar_proveedor'),
    path('listar_proveedor/',views.listar_proveedor,name='listar_proveedor'),
    path('login/',views.user_login,name='login'),
]

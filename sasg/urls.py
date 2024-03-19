from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from . import views

#from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('',views.sasg,name='asago'),
    path('prod_carne/', views.prod_carne, name='prod_carne'),
    path('prod_pollo/',views.prod_pollo,name='prod_pollo'),
    path('prod_cerdo/',views.prod_cerdo,name='prod_cerdo'),
    path('prod_chorizo/',views.prod_chorizo,name='prod_chorizo'),
    path('dashboard/',views.dashboard,name='dashboard'),
    
    #/-----usuarios------/
    path('recuperar_contrasena/',views.recuperar_contrasena,name='recuperar_contrasena'),
    path('listar_usuario/',views.listar_usuario,name='listar_usuario'),
    path('registrar_usuario/',views.registrar_usuario,name='registrar_usuario'),
    path('pre_editar_usuario/<str:idusuario>',views.pre_editar_usuario,name='pre_editar_usuario'),
    path('actualizar_usuario/<str:idusuario>/', views.actualizar_usuario,name='actualizar_usuario'),
    path('exportar-usuarios-pdf/', views.exportar_usuarios_pdf, name='exportar_usuarios_pdf'),
    
    
    
    #/-----productos------/
    path('listar_producto/',views.listar_producto,name='listar_producto'),
    path('registrar_producto/',views.registrar_producto,name='registrar_producto'),
    path('pre_editar_producto/<str:idproducto>',views.pre_editar_producto,name='pre_editar_producto'),
    path('actualizar_producto/<str:idproducto>',views.actualizar_producto,name='actualizar_producto'),
    path('exportar-productos-pdf/', views.exportar_productos_pdf, name='exportar_productos_pdf'),
    #/-----ventas------/
    path('listar_venta/',views.listar_venta,name='listar_venta'),
    path('registrar_venta/',views.registrar_venta,name='registrar_venta'),
    path('exportar-ventas-pdf/', views.exportar_ventas_pdf, name='exportar_ventas_pdf'),
    path('detalle_venta/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),
    
    #/-----Compras----/
    path('listar_compra/',views.listar_compra,name='listar_compra'),
    path('registrar_compra/',views.registrar_compra,name='registrar_compra'),
    path('exportar-compras-pdf/', views.exportar_compras_pdf, name='exportar_compras_pdf'),
    path('detalle_compra/<int:compra_id>/', views.detalle_compra, name='detalle_compra'),
     
    #/-----pedidos------/
    path('listar_pedido/',views.listar_pedido,name='listar_pedido'),
    path('pre_editar_pedido/<str:idpedido>',views.pre_editar_pedido,name='pre_editar_pedido'),
    path('actualizar_pedido/<str:idpedido>',views.actualizar_pedido,name='actualizar_pedido'),
    path('exportar-pedidos-pdf/', views.exportar_pedidos_pdf, name='exportar_pedidos_pdf'),
    path('carrito/', views.carrito, name='carrito'),
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('actualizar_cantidad_carrito/<int:producto_id>/', views.actualizar_cantidad_carrito, name='actualizar_cantidad_carrito'),
    path('eliminar_producto_carrito/<int:producto_id>/', views.eliminar_producto_carrito, name='eliminar_producto_carrito'),
    path('eliminar_todo_carrito/', views.eliminar_todo_carrito, name='eliminar_todo_carrito'),
    path('hacer_pedido/', views.hacer_pedido, name='hacer_pedido'),
    
    #/-----proveedores------/
    path('listar_proveedor/',views.listar_proveedor,name='listar_proveedor'),
    path('registrar_proveedor/',views.registrar_proveedor,name='registrar_proveedor'),
    path('pre_editar_proveedor/<str:idproveedor>',views.pre_editar_proveedor,name='pre_editar_proveedor'),
    path('actualizar_proveedor/<str:idproveedor>',views.actualizar_proveedor,name='actualizar_proveedor'),
    path('exportar-proveedores-pdf/', views.exportar_proveedores_pdf, name='exportar_proveedores_pdf'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.logout, name='logout'),
    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404 = 'sasg.views.pagina_no_encontrada'

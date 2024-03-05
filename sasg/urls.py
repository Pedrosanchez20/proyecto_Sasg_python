from django.urls import path

<<<<<<< HEAD
from .import views

urlpatterns = [
    path('',views.sasg,name='asago'),
    path('catPollo',views.catPollView,name='catPollo'),
    path('catCarne',views.catCarnView,name='catCarne'),
    path('catCerdo',views.catCerdView,name='catCerdo'),
    path('catChorizo',views.catChoView,name='catChorizo'),
    path('producto',views.prodView,name='producto'),
    path('pedidos',views.pedView,name='pedidos'),
    path('ventas',views.ventView,name='ventas'),
    path('usuarios',views.usuaView,name='usuarios'),
    path('listar_usuario/',views.listar_usuario, name='listar_usuario'),
]
=======
from .views import (asagoView, catCarnView, catCerdView, catChoView,
                    catPollView, pedView, prodView, ventView, 
                    proveesView, usuaView)

urlpatterns = [
    path('', asagoView,name='asago'),
    path('catPollo',catPollView,name='catPollo'),
    path('catCarne',catCarnView,name='catCarne'),
    path('catCerdo', catCerdView,name='catCerdo'),
    path('catChorizo',catChoView,name='catChorizo'),
    path('producto',prodView,name='producto'),
    path('pedidos',pedView,name='pedidos'),
    path('ventas',ventView,name='ventas'),
    path('usuarios',usuaView,name='usuarios'),
    path('proveedores',proveesView,name='proveedores'),
]
>>>>>>> 3c539f8a67e9379f9089003b240c8c0a99ec2db8

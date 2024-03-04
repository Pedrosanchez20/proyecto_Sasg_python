from django.urls import path

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
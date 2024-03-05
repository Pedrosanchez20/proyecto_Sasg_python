from django.urls import path

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

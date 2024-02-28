from django.urls import path

from .views import asagoView, catCarnView, prodView

urlpatterns = [
    path('', asagoView,name='asago'),
    path('catCarne',catCarnView,name='catCarne'),
    path('producto',prodView,name='producto'),
]
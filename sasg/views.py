from django.shortcuts import HttpResponse, render
from .models import Producto
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render


# Create your views here.
def asagoView(request):
    return render(request, 'sasg/index.html')
def catCarnView(request):
    return render(request, 'sasg/catcarne.html')
def catPollView(request):
    return render(request, 'sasg/catpollo.html')
def catCerdView(request):
    return render(request, 'sasg/catcerdo.html')
def catChoView(request):
    return render(request, 'sasg/catchorizo.html')
def prodView(request):
    producto = Producto.objects.all()
    data={
        'producto':producto,
    }
    return render(request, 'sasg/productos.html',data)

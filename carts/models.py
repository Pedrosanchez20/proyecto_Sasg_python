from django.db import models

# Create your models here.
from sasg.models import Usuarios, Producto

class Cart(models.Model):
    usuario = models.ForeignKey(Usuarios, null=True, blank=True, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto)
    subtotal = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    total = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return ''
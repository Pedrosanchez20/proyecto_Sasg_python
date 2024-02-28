from django.db import models

# Create your models here.
class Producto(models.Model):
    IdProducto = models.BigIntegerField()
    FechaRegistro = models.DateField()
    NomProducto = models.CharField(max_length=50)
    NomCategoria = models.CharField(max_length=50)
    cantidad = models.BigIntegerField()
    FechaVencimiento = models.DateField()
    Valorlibra = models.BigIntegerField()
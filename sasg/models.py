# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone


class Compra(models.Model):
    idcompra = models.AutoField(db_column='IdCompra', primary_key=True)  # Field name made lowercase.
    fechaemision = models.DateField(db_column='FechaEmision')  # Field name made lowercase.
    idproveedor = models.ForeignKey('Proveedor', models.DO_NOTHING, db_column='IdProveedor')  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=100)  # Field name made lowercase.
    valorproducto = models.IntegerField(db_column='ValorProducto')  # Field name made lowercase.
    valortotal = models.IntegerField(db_column='ValorTotal')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'compra'


class Pedido(models.Model):
    idpedido = models.AutoField(db_column='IdPedido', primary_key=True)  # Field name made lowercase.
    idusuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='IdUsuario')  # Field name made lowercase.
    fechaemision = models.DateField(db_column='FechaEmision')  # Field name made lowercase.
    descripcion = models.TextField(db_column='Descripcion')  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=50)  # Field name made lowercase.
    valortotal = models.IntegerField(db_column='ValorTotal')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pedido'


class Producto(models.Model):
    idproducto = models.AutoField(db_column='IdProducto', primary_key=True)  # Field name made lowercase.
    fecharegistro = models.DateField(default=timezone.now, null=True)  # Field name made lowercase.
    nomproducto = models.CharField(db_column='NomProducto', max_length=50)  # Field name made lowercase.
    nomcategoria = models.CharField(db_column='NomCategoria', max_length=10)  # Field name made lowercase.
    cantidad = models.CharField(max_length=50)
    fechavencimiento = models.DateField(db_column='FechaVencimiento')  # Field name made lowercase.
    valorlibra = models.IntegerField(db_column='Valorlibra')  # Field name made lowercase.
    foto_producto = models.ImageField(upload_to="productos",null=True) # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'producto'


class Proveedor(models.Model):
    idproveedor = models.IntegerField(db_column='IdProveedor', primary_key=True)  # Field name made lowercase.
    nomempresa = models.CharField(db_column='NomEmpresa', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'proveedor'


class Roles(models.Model):
    idrol = models.AutoField(db_column='IdRol', primary_key=True)  # Field name made lowercase.
    rolnombre = models.CharField(db_column='RolNombre', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'roles'


class Usuarios(models.Model):
    idusuario = models.AutoField(db_column='IdUsuario', primary_key=True)  # Field name made lowercase.
    rol = models.ForeignKey(Roles, models.DO_NOTHING, db_column='Rol')  # Field name made lowercase.
    nombres = models.CharField(db_column='Nombres', max_length=50)  # Field name made lowercase.
    apellidos = models.CharField(db_column='Apellidos', max_length=50)  # Field name made lowercase.
    fechanacimiento = models.DateField(db_column='FechaNacimiento')  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', max_length=100)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=20)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50)  # Field name made lowercase.
    contrasena = models.CharField(db_column='Contrasena', max_length=50)  # Field name made lowercase.
    estado = models.CharField(max_length=13)

    class Meta:
        managed = False
        db_table = 'usuarios'


class Venta(models.Model):
    idventa = models.AutoField(db_column='IdVenta', primary_key=True)  # Field name made lowercase.
    fechaemision = models.DateField(db_column='FechaEmision')  # Field name made lowercase.
    idpedido = models.ForeignKey(Pedido, models.DO_NOTHING, db_column='IdPedido')  # Field name made lowercase.
    idcliente = models.IntegerField(db_column='IdCliente')  # Field name made lowercase.
    idproducto = models.ForeignKey(Producto, models.DO_NOTHING, db_column='IdProducto')  # Field name made lowercase.
    producto = models.CharField(db_column='Producto', max_length=50)  # Field name made lowercase.
    cantidad = models.IntegerField(db_column='Cantidad')  # Field name made lowercase.
    valorproducto = models.IntegerField(db_column='ValorProducto')  # Field name made lowercase.
    valortotal = models.IntegerField(db_column='ValorTotal')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'venta'


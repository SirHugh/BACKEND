from django.db import models
from academico.models import Matricula, Cliente, Grado
from accounts.models import User

# Create your models here.
#
# ------------------------------------Producto Models ---------------------------- 
#
class Producto(models.Model):
    TIPO_PRODUCTO = [
        ('PR', 'PRODUCTO'),
        ('AR', 'ARANCEL'),
        ('AC', 'ACTIVIDAD')
    ]
    
    id_producto = models.AutoField(primary_key=True)
    # id_grado = models.ManyToManyField(Grado, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=254, null=True, blank=True)
    tipo = models.CharField(max_length=2, choices=TIPO_PRODUCTO)
    es_activo = models.BooleanField()
    stock = models.IntegerField(null=True, blank=True)
    precio = models.IntegerField(null=True, blank=True)
    grados = models.ManyToManyField(Grado, related_name='productos')
    es_mensual = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre
 
#
# ------------------------------------ Comprobantes Models ---------------------------- 
#   

    
class Timbrado(models.Model):
    id_timbrado = models.AutoField(primary_key=True)
    nro_timbrado = models.IntegerField()
    fecha_desde = models.DateField(auto_now=False, auto_now_add=False)
    fecha_hasta = models.DateField(auto_now=False, auto_now_add=False)
    es_activo = models.BooleanField()
    establecimiento =models.IntegerField(default=1)
    punto_expedicion=models.IntegerField(default=1)
    numero_inicial = models.IntegerField()
    numero_final = models.IntegerField(null=True, blank=True)
    ultimo_numero = models.IntegerField(null=True, blank=True, default=0)


class Comprobante(models.Model):
    id_comprobante = models.AutoField(primary_key=True)
    id_timbrado = models.ForeignKey(Timbrado, on_delete=models.CASCADE, null=True, blank=True)
    nro_factura = models.IntegerField(null=True, blank=True)
    id_user = models.ForeignKey(User,  on_delete=models.CASCADE)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now=False, auto_now_add=False)
    tipo_pago = models.CharField( max_length=50)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
     
#
# ------------------------------------ Arancel Pagos Models ---------------------------- 
#
class Arancel(models.Model):
    id_arancel = models.AutoField(primary_key=True)
    id_matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE) 
    id_comprobante = models.ForeignKey(Comprobante, on_delete=models.CASCADE, null=True, blank=True)
    fecha_vencimiento = models.DateField( )
    nro_cuota = models.IntegerField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    es_activo = models.BooleanField()

    def __str__(self):
        return self.id_producto.nombre
    
#
# ------------------------------------ Ventas Models ---------------------------- 
#
class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    id_matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE)
    nro_pagos = models.IntegerField()
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)

class DetalleVenta(models.Model):
    id_detalleVenta = models.AutoField(primary_key=True)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()

class PagoVenta(models.Model):
    id_pago = models.AutoField(primary_key=True)
    id_comprobante = models.ForeignKey(Comprobante, on_delete=models.CASCADE)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    fecha_vencimiento = models.DateField()
    nro_pago = models.IntegerField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    es_activo = models.BooleanField()
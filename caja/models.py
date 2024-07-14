from django.db import models
from academico.models import Matricula, Cliente, Grado
from accounts.models import User
from django.utils import timezone
import datetime
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

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
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=254, null=True, blank=True)
    tipo = models.CharField(max_length=2, choices=TIPO_PRODUCTO)
    iva = models.IntegerField(default=0)
    es_activo = models.BooleanField()
    stock = models.IntegerField(null=True, blank=True)
    stock_minimo = models.IntegerField(null=True, blank=True)
    precio = models.IntegerField(null=True, blank=True)
    grados = models.ManyToManyField(Grado, related_name='productos', blank=True)
    es_mensual = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre
#
# ------------------------------------ AjusteDetalle Model ---------------------------- 
#   
class BajaInventario(models.Model):
    id_bajaInventario = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cantidad = models.IntegerField()    
    razon = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True)
 
#
# ------------------------------------ Timbrado Model ---------------------------- 
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

#
# ------------------------------------ Flujo caja Model ---------------------------- 
#   

class FlujoCaja(models.Model):
    id_flujoCaja = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    hora_apertura = models.TimeField(auto_now_add=True)
    hora_cierre = models.TimeField(blank=True, null=True)
    monto_apertura = models.DecimalField(max_digits=10, decimal_places=2)
    monto_cierre = models.DecimalField(max_digits=10, decimal_places=2)
    entrada = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    salida = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    es_activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['-fecha']

    def save(self, *args, **kwargs):

        # restringe la actualizacion del flujoCaja fuera del dia de creacion
        if self.pk and self.fecha!= datetime.datetime.now().date():
            raise ValidationError('No es posible modificar un flujo de caja anterior')

        if not self.pk:  # solo en la creacion, no en el update<
            if FlujoCaja.objects.filter(fecha=datetime.datetime.now().date()).exists():
                raise ValidationError('Ya existe un flujo de caja para hoy')
            self.monto_cierre = self.monto_apertura 

        if not self.es_activo:
            self.hora_cierre = datetime.datetime.now().time()
        else:
            self.hora_cierre = None

        super().save(*args, **kwargs)

    @classmethod
    def get_current(cls):
        date = datetime.datetime.now().date()  
        return cls.objects.filter(fecha=date).first() 

#
# ------------------------------------ Comprobantes Model ---------------------------- 
#   

class Comprobante(models.Model):
    id_comprobante = models.AutoField(primary_key=True)
    id_timbrado = models.ForeignKey(Timbrado, on_delete=models.CASCADE, null=True, blank=True)
    id_flujoCaja = models.ForeignKey(FlujoCaja, on_delete=models.CASCADE, null=True, blank=True)
    nro_factura = models.IntegerField(null=True, blank=True)
    id_user = models.ForeignKey(User,  on_delete=models.CASCADE)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now=False, auto_now_add=False)
    hora = models.TimeField(auto_now_add=True, blank=True, null=True)
    tipo_pago = models.CharField( max_length=50)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-fecha']
     
#
# ------------------------------------ Arancel Pagos Model ---------------------------- 
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
# ------------------------------------ Ventas Model ---------------------------- 
#

class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    id_matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE)
    nro_pagos = models.IntegerField()
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
 
#
# ------------------------------------ Detalle Venta Model ---------------------------- 
#   
    
class DetalleVenta(models.Model):
    id_detalleVenta = models.AutoField(primary_key=True)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
 
#
# ------------------------------------ Pago Venta Model ---------------------------- 
#   
    
class PagoVenta(models.Model):
    id_pago = models.AutoField(primary_key=True)
    id_comprobante = models.ForeignKey(Comprobante, on_delete=models.CASCADE, null=True)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    fecha_vencimiento = models.DateField()
    nro_pago = models.IntegerField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    es_activo = models.BooleanField()

    
#
# ------------------------------------ Compra Model ---------------------------- 
#   

class Compra(models.Model):
    id_compra = models.AutoField(primary_key=True)
    id_flujoCaja = models.ForeignKey(FlujoCaja, on_delete=models.CASCADE, related_name="compra", null=True, blank=True)
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    nro_factura = models.IntegerField()
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tiempo_alta = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-tiempo_alta']
    
#
# ------------------------------------ DetalleCompra Model ---------------------------- 
#   

class DetalleCompra(models.Model):
    id_detalleCompra = models.AutoField(primary_key=True)
    id_compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name="detalleCompra")
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="detalleCompra")
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)


#
# ------------------------------------ Extraccion Model ---------------------------- 
#   

class Extraccion(models.Model):
    id_extraccion = models.AutoField(primary_key=True)
    id_flujoCaja = models.ForeignKey(FlujoCaja, on_delete=models.CASCADE, related_name="extraccion")
    fecha = models.DateField()
    hora = models.TimeField(auto_now=False, auto_now_add=False)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    concepto = models.TextField()
    nro_factura = models.IntegerField(blank=True, null=True)

class TipoActividad(models.Model):
    id_tipoActividad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=254)

class Actividad(models.Model):
    id_actividad = models.AutoField(primary_key=True)
    id_tipoActividad = models.ForeignKey(TipoActividad, on_delete=models.CASCADE)
    id_periodo = models.ForeignKey("academico.Periodo", on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_grado = models.ForeignKey("academico.Grado", on_delete=models.CASCADE)
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    es_activo = models.BooleanField(default=False)
    
    # class Meta:
    #     unique_together = (('id_tipoActividad', 'id_periodo', 'id_grado' ),)
    
class PagoActividad(models.Model):
    id_pagoActividad = models.AutoField(primary_key=True)
    id_actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name='PagoActividad')
    id_matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE)
    id_comprobante = models.ForeignKey(Comprobante, on_delete=models.CASCADE)
    fecha_pago = models.DateField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)


    
    
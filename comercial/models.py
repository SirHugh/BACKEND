from django.db import models

# Create your models here.
class ControlStock(models.Model):
    id_controlStock = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    fecha = models.DateField(auto_now=False, auto_now_add=True)
    es_activo = models.BooleanField(default=True)
    
class DetalleControl(models.Model):
    id_detalleControl = models.AutoField(primary_key=True)
    id_controlStock = models.ForeignKey("ControlStock", on_delete=models.CASCADE)
    id_producto = models.ForeignKey("caja.Producto", on_delete=models.CASCADE)
    stock = models.IntegerField()
    cantidad_contada = models.IntegerField()
    
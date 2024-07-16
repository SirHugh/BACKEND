from rest_framework import serializers
from .models import ControlStock, DetalleControl
from caja.models import Producto

class ControlStockSerializer(serializers.ModelSerializer):
    # cantidad_productos = serializers.SerializerMethodField()
    usuario = serializers.SerializerMethodField()
    
    class Meta:
        model = ControlStock
        fields = ['id_controlStock', 'fecha', 'es_activo', 'id_usuario', 'usuario', 'cantidad_productos']
    
    # def get_cantidad_productos(self, obj):
    #     return DetalleControl.objects.filter(id_controlStock=obj.id_controlStock).count()
    
    def get_usuario(self, obj):
        return obj.id_usuario.__str__()
        
class DetalleControlSerializer(serializers.ModelSerializer):
    producto = serializers.SerializerMethodField()
    
    class Meta:
        model = DetalleControl
        fields = ['id_detalleControl', 'stock', 'cantidad_contada', 'id_controlStock', 'id_producto', 'producto']
        
    def get_producto(self, obj):
        return getattr(obj.id_producto, 'nombre', None)
from rest_framework import serializers
from .models import ControlStock, DetalleControl 

class ControlStockSerializer(serializers.ModelSerializer): 
    usuario = serializers.SerializerMethodField()
    
    class Meta:
        model = ControlStock
        fields = ['id_controlStock', 'fecha', 'es_activo', 'id_usuario', 'usuario', 'cantidad_productos']
  
    def get_usuario(self, obj):
        return obj.id_usuario.__str__()
        
class DetalleControlSerializer(serializers.ModelSerializer):
    producto = serializers.SerializerMethodField()
    
    class Meta:
        model = DetalleControl
        fields = ['id_detalleControl', 'stock', 'cantidad_contada', 'id_controlStock', 'id_producto', 'producto']
        
    def get_producto(self, obj):
        return getattr(obj.id_producto, 'nombre', None)
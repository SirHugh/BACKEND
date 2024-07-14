from rest_framework import serializers
from .models import ControlStock, DetalleControl
from caja.models import Producto

class ControlStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlStock
        fields = '__all__'
        
class DetalleControlSerializer(serializers.ModelSerializer):
    producto = serializers.SerializerMethodField()
    
    class Meta:
        model = DetalleControl
        fields = ['id_detalleControl', 'stock', 'cantidad_contada', 'id_controlStock', 'id_producto', 'producto']
        
    def get_producto(self, obj):
        return getattr(obj.id_producto, 'nombre', None)
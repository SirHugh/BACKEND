from rest_framework import serializers
from .models import   Arancel, Timbrado, Producto, Comprobante, Venta, DetalleVenta, PagoVenta
from academico.models import Alumno, Matricula 

class TimbradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timbrado
        fields = '__all__'

class ComprobanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comprobante
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class ArancelInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arancel
        fields = '__all__' 

class ArancelOutputSerializer(serializers.ModelSerializer):
    alumno = serializers.SerializerMethodField()
    nombre = serializers.SerializerMethodField()

    class Meta:
        model = Arancel
        fields = ["id_arancel", "id_comprobante", "alumno", "nombre", "fecha_vencimiento", "nro_cuota", "monto", "es_activo"]

    def get_alumno(self, obj):
        try:
            alumno = obj.id_matricula.id_alumno.__str__()
            return alumno
        except Alumno.DoesNotExist:
            return None
    
    def get_nombre(sefl, obj):
        try:
            producto = obj.id_producto.__str__()
            return producto
        except Producto.DoesNotExist:
            return None

class VentaInputSerializar(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'

class DetalleVentaSerializar(serializers.ModelSerializer):
     class Meta:
         model= DetalleVenta
         fields = ['id_producto', 'cantidad', 'precio']

class PagoVentaInputSerializar(serializers.ModelSerializer):
    class Meta:
        model = PagoVenta
        fields = ['fecha_vencimiento', 'nro_pago', 'monto', 'es_activo']

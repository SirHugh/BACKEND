from rest_framework import serializers
from .models import   Arancel, Timbrado, Producto, Comprobante 
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
        fields = ["id_arancel", "alumno", "nombre", "fecha_vencimiento", "nro_cuota", "monto", "es_activo"]

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


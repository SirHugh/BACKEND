from rest_framework import serializers
from .models import   Arancel, Timbrado, Producto, Comprobante, Venta, DetalleVenta, PagoVenta
from academico.models import Alumno, Matricula, Cliente 

class TimbradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timbrado
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




class PagoVentaInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagoVenta
        fields = ['fecha_vencimiento', 'nro_pago', 'monto', 'es_activo']

class PagoVentaOutputSerializer(serializers.ModelSerializer):
    alumno = serializers.SerializerMethodField()
    descripcion = serializers.SerializerMethodField()
    nroPagos = serializers.SerializerMethodField()

    class Meta:
        model = PagoVenta
        fields = ['id_pago','id_venta', 'nroPagos', 'descripcion', 'alumno', 'fecha_vencimiento', 'nro_pago', 'monto', 'es_activo']

    def get_alumno(self, obj):
        try:
            alumno = obj.id_venta.id_matricula.id_alumno.__str__()
            return alumno
        except Alumno.DoesNotExist:
            return None
    
    def get_descripcion(self, obj):
        try:
            detalle = DetalleVenta.objects.filter(id_venta=obj.id_venta) 
            return DetalleVentaSerializer(detalle, many=True).data
        except DetalleVenta.DoesNotExist:
            return None
        
    def get_nroPagos(self, obj):
        try:
            nroPagos = PagoVenta.objects.filter(id_venta=obj.id_venta).count()
            return nroPagos
        except Venta.DoesNotExist:
            return None
                
class DetalleVentaSerializer(serializers.ModelSerializer):
    producto = serializers.SerializerMethodField()

    class Meta:
         model= DetalleVenta
         fields = ['producto', 'cantidad', 'precio']
    
    def get_producto(self, obj):
        try:
            producto = obj.id_producto.__str__()
            return producto
        except Producto.DoesNotExist:
            return None
    
class VentaInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'

class VentaOutputSerializer(serializers.ModelSerializer):
    alumno = serializers.SerializerMethodField()
    detalle = serializers.SerializerMethodField()
    pagos = serializers.SerializerMethodField()

    class Meta:
        model = Venta
        fields = ["id_venta", "id_matricula", 
                  "alumno", "fecha", "monto", "detalle", "pagos"]

    def get_alumno(self, obj):
        try:
            alumno = obj.id_matricula.id_alumno.__str__()
            return alumno
        except Alumno.DoesNotExist:
            return None
    
    def get_detalle(self, obj):
        try:
            detalle = DetalleVenta.objects.filter(id_venta=obj.id_venta) 
            return DetalleVentaSerializer(detalle, many=True).data
        except DetalleVenta.DoesNotExist:
            return None
    
    def get_pagos(self, obj):
        try:
            pagos = PagoVenta.objects.filter(id_venta=obj.id_venta) 
            return PagoVentaInputSerializer(pagos, many=True).data
        except PagoVenta.DoesNotExist:
            return None
        
class ComprobanteInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comprobante
        fields = '__all__'

class ComprobanteOutputSerializer(serializers.ModelSerializer):
    aranceles = serializers.SerializerMethodField()
    ventas = serializers.SerializerMethodField()
    cliente = serializers.SerializerMethodField()

    class Meta:
        model = Comprobante
        fields = ['id_comprobante', 'fecha', 'nro_factura', 'tipo_pago', 'monto', 'cliente', 'aranceles', 'ventas']

    def get_cliente(self, obj):
        try:
            cliente = obj.id_cliente.__str__()
            return cliente
        except Cliente.DoesNotExist:
            return None

    def get_aranceles(self, obj):
        try:
            aranceles = Arancel.objects.filter(id_comprobante=obj.id_comprobante) 
            return ArancelOutputSerializer(aranceles, many=True).data
        except Arancel.DoesNotExist:
            return None
        
    def get_ventas(self, obj):
        try:
            ventas = PagoVenta.objects.filter(id_comprobante=obj.id_comprobante)
            return PagoVentaOutputSerializer(ventas, many=True).data
        except PagoVenta.DoesNotExist:
            return None
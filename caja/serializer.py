from rest_framework import serializers
from .models import   Arancel, AjusteDetalle, Timbrado, Producto, Comprobante, Venta, DetalleVenta, PagoVenta, Compra, DetalleCompra, FlujoCaja, Extraccion, TipoActividad, Actividad, PagoActividad
from academico.models import Alumno, Matricula, Cliente, Grado, Periodo
from accounts.models import User

class TimbradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timbrado
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class AjusteDetalleSerializer(serializers.ModelSerializer):
    id_producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())
    id_usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    cantidad = serializers.IntegerField()
    fecha = serializers.DateTimeField(required=False)

    class Meta:
        model = AjusteDetalle        
        fields = '__all__'
        
class AjusteOutputSerializer(serializers.ModelSerializer):
    producto = serializers.SerializerMethodField()
    
    class Meta:
        model = AjusteDetalle
        fields = ['id_ajusteDetalle', 'id_producto', 'producto', 'razon', 'fecha', 'cantidad']
        
    def get_producto(self, obj):
        try:
            producto = obj.id_producto.__str__()
            return producto
        except Producto.DoesNotExist:
            return None

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
    actividades =serializers.SerializerMethodField()
    cliente = serializers.SerializerMethodField()

    class Meta:
        model = Comprobante
        fields = ['id_comprobante', 'fecha', 'hora', 'nro_factura', 'tipo_pago', 'monto', 'cliente', 'aranceles', 'ventas', 'actividades']

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

    def get_actividades(self, obj):
        try:
            actividades = PagoActividad.objects.filter(id_comprobante=obj.id_comprobante)
            return PagoActividadOutputSerializer(actividades, many=True).data
        except PagoActividad.DoesNotExist:
            return None
# 
# 
# ----- Detalle Compra serializers
# 
# 
class DetalleCompraInputSerializer(serializers.ModelSerializer):
    id_producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())

    class Meta:
        model = DetalleCompra
        fields = ['id_producto', 'cantidad', 'precio']

class DetalleCompraOutputSerializer(serializers.ModelSerializer):
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
    
# 
# 
# ----- Compra serializers
# 
# 

class CompraInputSerializer(serializers.ModelSerializer):
    id_flujoCaja = serializers.PrimaryKeyRelatedField(queryset=FlujoCaja.objects.all(), required=False, allow_null=True)
    tiempo_alta = serializers.DateTimeField(read_only=True, required=False)

    class Meta:
        model = Compra
        fields = ['id_compra','fecha', 'tiempo_alta', 'monto', 'nro_factura', 'id_flujoCaja', 'id_usuario']

class CompraOutputSerializer(serializers.ModelSerializer):
    detalle = serializers.SerializerMethodField()

    class Meta:
        model = Compra
        fields = ["id_compra", 'id_flujoCaja', 'fecha', 'tiempo_alta', 'nro_factura', 'id_usuario', 'monto', 'detalle']

    def get_detalle(self, obj):
        try:
            detalle = DetalleCompra.objects.filter(id_compra=obj.id_compra) 
            return DetalleCompraOutputSerializer(detalle, many=True).data
        except DetalleCompra.DoesNotExist:
            return None
# 
# 
# ----- Extracciones Serializers
# 
# 

class ExtraccionInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extraccion
        fields = '__all__'

# 
# 
# ----- Flujo Caja Serializers
# 
# 

class FlujoCajaNormalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlujoCaja
        fields = '__all__'

class FlujoCajaInputSerializer(serializers.ModelSerializer): 
    id_usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True, allow_null=True)
    monto_apertura = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)

    class Meta:
        model = FlujoCaja
        fields = ['id_usuario', 'monto_apertura']


class FlujoCajaOutputSerializer(serializers.ModelSerializer):
    facturas = serializers.SerializerMethodField()
    compras = serializers.SerializerMethodField()
    extracciones = serializers.SerializerMethodField()

    class Meta:
        model = FlujoCaja
        fields = [ 'id_flujoCaja', 'id_usuario', 'fecha', 'hora_apertura', 'hora_cierre', 'monto_apertura', 
                  'monto_cierre', 'entrada', 'salida', 'es_activo', 'facturas', 'compras', 'extracciones']
    
    def get_compras(self, obj):
        try:
            compras = Compra.objects.filter(id_flujoCaja=obj.id_flujoCaja)
            return CompraInputSerializer(compras, many=True).data
        except Compra.DoesNotExist:
            return None
    
    def get_facturas(self, obj):
        try:
            facturas = Comprobante.objects.filter(id_flujoCaja=obj.id_flujoCaja)
            return ComprobanteInputSerializer(facturas, many=True).data
        except Comprobante.DoesNotExist:
            return None
    
    def get_extracciones(self, obj):
        try:
            extracciones = Extraccion.objects.filter(id_flujoCaja=obj.id_flujoCaja)
            return ExtraccionInputSerializer(extracciones, many=True).data
        except Extraccion.DoesNotExist:
            return None
 
# 
# 
# ----- Actividades Serializers
# 
# 
class TipoActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoActividad
        fields = '__all__'
        
# 
# 
# ----- Actividades Serializers
# 
# 
class ActividadInputSerializer(serializers.ModelSerializer):
    id_usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    id_periodo = serializers.PrimaryKeyRelatedField(queryset=Periodo.objects.all(), required=False, allow_null=True)
    id_tipoActividad = serializers.PrimaryKeyRelatedField(queryset=TipoActividad.objects.all(), required=True, allow_null=False)
    monto = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    es_activo = serializers.BooleanField(required=False)
    
    class Meta: 
        model = Actividad
        fields = ["id_tipoActividad", "id_usuario", "id_grado", "fecha", "monto", 'id_periodo', 'es_activo']

class ActividadOutputDetailSerializer(serializers.ModelSerializer):
    grado = serializers.SerializerMethodField()
    actividad = serializers.SerializerMethodField()
    pagos = serializers.SerializerMethodField()
    
    class Meta:
        model = Actividad
        fields = ['id_actividad', 'grado', 'fecha', 'monto', 'es_activo', 'actividad', 'pagos' ]

    def get_grado(self, obj):
        try:
            grado = obj.id_grado.__str__()
            return grado
        except Grado.DoesNotExist:
            return None
    
    def get_actividad(self, obj):
        try:
            tipoActividad = obj.id_tipoActividad.nombre
            return tipoActividad
        except TipoActividad.DoesNotExist:
            return None
        
    def get_pagos(self, obj):
        try:
            pagos = PagoActividad.objects.filter(id_actividad=obj.id_actividad)
            return PagoActividadOutputSerializer(pagos, many=True).data
        except PagoActividad.DoesNotExist:
            return None

class ActividadOutputSerializer(serializers.ModelSerializer):
    grado = serializers.SerializerMethodField()
    actividad = serializers.SerializerMethodField()
    
    class Meta:
        model = Actividad
        fields = ['id_actividad', 'grado', 'fecha', 'monto', 'es_activo', 'actividad', ]
        
    def get_grado(self, obj):
        try:
            grado = obj.id_grado.__str__()
            return grado
        except Grado.DoesNotExist:
            return None
    
    def get_actividad(self, obj):
        try:
            tipoActividad = obj.id_tipoActividad.nombre
            return tipoActividad
        except TipoActividad.DoesNotExist:
            return None
    
# 
# 
# ----- Actividades Serializers
# 
# 
class PagoActividadInputSerializer(serializers.ModelSerializer):
    id_actividad = serializers.PrimaryKeyRelatedField(queryset=Actividad.objects.all(), required=True,)
    id_matricula = serializers.PrimaryKeyRelatedField(queryset=Matricula.objects.all(), required=True,)
    id_comprobante = serializers.PrimaryKeyRelatedField(queryset=Comprobante.objects.all(), required=False,)
    monto = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    
    class Meta:
        model = PagoActividad
        fields = ['id_actividad', 'id_matricula', 'id_comprobante', 'monto'] 

class PagoActividadOutputSerializer(serializers.ModelSerializer):
    actividad = serializers.SerializerMethodField()
    alumno = serializers.SerializerMethodField()
    
    class Meta:
        model = PagoActividad
        fields = ['id_pagoActividad', 'actividad', 'alumno', 'monto', 'fecha_pago']
        
    def get_actividad(self, obj):
        try:
            actividad = obj.id_actividad.id_tipoActividad.nombre
            return actividad
        except PagoActividad.DoesNotExist:
            return None
    
    def get_alumno(self, obj):
        try:
            alumno = obj.id_matricula.id_alumno.__str__()
            return alumno
        except PagoActividad.DoesNotExist:
            return None
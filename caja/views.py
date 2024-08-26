from rest_framework import status, generics, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import DescuentoBeca, FormaPago, Producto, Arancel, Timbrado, Comprobante, PagoVenta, Venta, DetalleVenta, Compra, FlujoCaja, BajaInventario
from .serializer import DescuentoBecaInputSerializer, ProductoSerializer, ArancelInputSerializer, ArancelOutputSerializer, TimbradoSerializer, VentaInputSerializer, DetalleVentaSerializer, PagoVentaInputSerializer 
from . import serializer
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, DjangoObjectPermissions
from django_filters.rest_framework import DjangoFilterBackend
from academico.views import OptionalPagination
from django.db.models import Q
# ---------------------------------------------
# ---------vistas de productos-----------------
# ---------------------------------------------

class ProductoListCreateView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Producto.objects.all().order_by('codigo')
    serializer_class = ProductoSerializer
    pagination_class = OptionalPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter] 
    search_fields = ['nombre','descripcion']
    filterset_fields = ['tipo', 'grados','es_activo']
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        codigo = instance.codigo
        instance.codigo = f"{codigo}-{instance.id_producto}"
        instance.save()
        return Response(serializer.data)

class ProductoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data) 
        serializer.is_valid(raise_exception=True) 
        instance = serializer.save() 
        codigo = instance.codigo
        instance.codigo = f"{codigo}-{instance.id_producto}"
        instance.save()
        return Response(serializer.data) 

# ---------------------------------------------
# ---------vistas de Ajuste------------------
# ---------------------------------------------

class BajaInventarioListCreateView(generics.ListCreateAPIView):
    queryset = BajaInventario.objects.all().order_by('-fecha')
    serializer_class = serializer.BajaInventarioSerializer
    # permission_classes = [IsAuthenticated, DjangoModelPermissions]
    pagination_class = OptionalPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id_producto__nombre', 'razon']
     
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializer.BajaInventarioOutputSerializer
        else:
            return self.serializer_class
    
    def create(self, request, *args, **kwargs):
        ajustes = request.data
        serializer = self.serializer_class(data=ajustes, many=True)
        serializer.is_valid(raise_exception=True)
    
        for ajuste in ajustes:
            producto = Producto.objects.get(pk=ajuste['id_producto'])
            producto.stock += ajuste['cantidad']
            producto.save()

        serializer.save(id_usuario=self.request.user)
        return Response({'message':'Guardado Exitoso' }, status=status.HTTP_201_CREATED)

class BajaInventarioDetailView(generics.RetrieveUpdateAPIView):
    queryset = BajaInventario.objects.all()
    serializer_class = serializer.BajaInventarioOutputSerializer
    
# ---------------------------------------------
# ---------vistas de Timbrado------------------
# ---------------------------------------------

class TimbradoListCreateView(generics.ListCreateAPIView):
    queryset = Timbrado.objects.all().order_by('-es_activo')
    serializer_class = TimbradoSerializer
    pagination_class = OptionalPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter] 
    filterset_fields = ['es_activo']

class TimbradoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Timbrado.objects.all()
    serializer_class = TimbradoSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if Timbrado.objects.filter(es_activo=True).exclude(pk=instance.pk).exists():
            return Response({'error': 'Ya existe un timbrado activo'}, status=status.HTTP_400_BAD_REQUEST)

        if not instance.es_activo and serializer.validated_data['es_activo']:
            instance.es_activo = True
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        return super().update(request, *args, **kwargs)
 
# ---------------------------------------------
# ---------vistas de Comprobante--------------- 
# ---------------------------------------------

class ComprobanteListCreateView(generics.ListCreateAPIView):
    queryset = Comprobante.objects.all()
    serializer_class = serializer.ComprobanteInputSerializer
    pagination_class = OptionalPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter] 
    search_fields = ['^id_cliente__nombre','^id_cliente__apellido', 'id_cliente__cedula','id_cliente__ruc']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializer.ComprobanteOutputSerializer
        else:
            return self.serializer_class

    def create(self, request, *args, **kwargs):
        comprobante = request.data.get('comprobante')
        serializer = self.get_serializer(data=comprobante)
        serializer.is_valid(raise_exception=True)
        id_timbrado = comprobante.get('id_timbrado');
        flujoCaja = FlujoCaja.get_current()
        if flujoCaja is None:
            return Response({'error': 'No hay un flujo de caja activo'}, status=status.HTTP_404_NOT_FOUND)

        aranceles = request.data.get('aranceles',[])
        pagoventas = request.data.get('pagoventas',[])
        actividades = request.data.get('actividades', [])
        descuentos = request.data.get('descuentos', []) 

        if not aranceles and not pagoventas and not actividades:
            return Response({'error':'No se encontradon pagos'}, status=status.HTTP_404_NOT_FOUND)
        
        if id_timbrado: 
            timbrado = Timbrado.objects.get(pk=id_timbrado)
            if not timbrado.es_activo:
                return Response({'error': 'El timbrado no esta activo'}, status=status.HTTP_400_BAD_REQUEST) 
            if timbrado.ultimo_numero == 0:
                serializer.validated_data['nro_factura'] = timbrado.ultimo_numero = timbrado.numero_inicial
            else:
                serializer.validated_data['nro_factura'] = timbrado.ultimo_numero = timbrado.ultimo_numero + 1
            timbrado.save()

        serializer.validated_data['id_flujoCaja'] = flujoCaja
        flujoCaja.monto_flujoCaja += comprobante['monto']
        flujoCaja.entrada += comprobante['monto']
        
        flujoCaja.save() 
        invoice = serializer.save()

        if aranceles:
            for arancel in aranceles:
                payment = Arancel.objects.get(pk=arancel)
                payment.id_comprobante = invoice 
                payment.es_activo = False
                payment.save()
        
        if pagoventas:
            for pago in pagoventas:
                payment = PagoVenta.objects.get(pk=pago)
                payment.id_comprobante = invoice 
                payment.es_activo = False
                payment.save()
        
        if actividades:
            for pago in actividades:
                serializer = PagoActividadInputSerializer(data=pago)
                serializer.is_valid() 
                serializer.validated_data['id_comprobante'] = invoice  
                serializer.save()
        
        if descuentos:
            for descuento in descuentos:
                d_beca = DescuentoBecaInputSerializer(data=descuento)
                d_beca.is_valid() 
                d_beca.save()
                
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ComprobanteDetailView(generics.RetrieveUpdateAPIView):
    queryset = Comprobante.objects.all()
    serializer_class = serializer.ComprobanteInputSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializer.ComprobanteOutputSerializer
        else:
            return self.serializer_class

# ---------------------------------------------
# ---------vistas de Arancel-------------------
# ---------------------------------------------

class ArancelListCreateView(generics.ListCreateAPIView):
    queryset = Arancel.objects.all().order_by('fecha_vencimiento')
    serializer_class = ArancelInputSerializer
    pagination_class = OptionalPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter] 
    search_fields = ['=id_matricula__id_alumno__cedula', '^id_matricula__id_alumno__nombre', '^id_matricula__id_alumno__apellido']
    filterset_fields = ['es_activo', 'id_comprobante', 'id_matricula']
     
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ArancelOutputSerializer
        else:
            return self.serializer_class

    def create(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        month = self.request.query_params.get('month', None)
        if month is not None:
            queryset =  self.queryset.filter(Q(fecha_vencimiento__month=month) | Q(fecha_vencimiento__month__lt=month))
            return queryset
        return self.queryset


class ArancelDetailView(generics.RetrieveUpdateAPIView):
    queryset = Arancel.objects.all()
    serializer_class = ArancelInputSerializer

    def get_serializer_class(self):
            if self.request.method == 'GET':
                return ArancelOutputSerializer
            else:
                return self.serializer_class 
            
# ---------------------------------------------
# -----------vistas de Ventas------------------
# ---------------------------------------------

class VentaListCreateView(generics.ListCreateAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaInputSerializer
    pagination_class = OptionalPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter] 
    search_fields = ['^id_matricula__id_alumno__cedula', '^id_matricula__id_alumno__nombre', '^id_matricula__id_alumno__apellido']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializer.VentaOutputSerializer
        else:
            return self.serializer_class

    def create(self, request, *args, **kwargs):
         
        venta = request.data.get('venta')
        ventaSerializer = self.get_serializer(data=venta)
        ventaSerializer.is_valid(raise_exception=True)

        detalleList = request.data.get('detalle', [])
        if not detalleList:
            return Response({'error':'No se encontro detalle de venta'}, status=status.HTTP_404_NOT_FOUND)
        for detalle in detalleList:
            detalleSerializer =  DetalleVentaSerializer(data=detalle);
            detalleSerializer.is_valid(raise_exception=True)
            producto = Producto.objects.get(pk=detalle['id_producto']);
            cantidad = detalle['cantidad']
            if producto.stock < cantidad:
                return Response({'error':'No hay suficiente stock para la venta'}, status=status.HTTP_400_BAD_REQUEST)

        pagosList = request.data.get('pagos', [])
        if not pagosList:
            return Response({'error':'No se encontro pagos de venta'}, status=status.HTTP_404_NOT_FOUND)
        for pago in pagosList:
            pagoSerializer =  PagoVentaInputSerializer(data=pago);
            pagoSerializer.is_valid(raise_exception=True)

        venta = ventaSerializer.save()

        for detalle in detalleList:
            detalleSerializer =  DetalleVentaSerializer(data=detalle);
            detalleSerializer.is_valid(raise_exception=True)
            detalleSerializer.validated_data['id_venta'] = venta
            detalleSerializer.validated_data['id_producto'] = Producto.objects.get(pk=detalle['id_producto'])
            detalleSerializer.validated_data['precio'] = Producto.objects.get(pk=detalle['id_producto']).precio
            detalleSerializer.save()
            producto = Producto.objects.get(pk=detalle['id_producto']);
            producto.stock = producto.stock - detalle['cantidad']
            producto.save()
        
        for pago in pagosList:
            pagoSerializer =  PagoVentaInputSerializer(data=pago);
            pagoSerializer.is_valid(raise_exception=True)
            pagoSerializer.validated_data['id_venta'] = venta  
            pagoSerializer.save()
        
        return Response(ventaSerializer.data, status=status.HTTP_201_CREATED)

class VentaDetailView(generics.RetrieveUpdateAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaInputSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializer.VentaOutputSerializer
        else:
            return self.serializer_class
        

# ---------------------------------------------
# -----------vistas de Pagos por Ventas------------------
# ---------------------------------------------

class PagoVentaListView(generics.ListAPIView):
    queryset = PagoVenta.objects.all()
    serializer_class = serializer.PagoVentaOutputSerializer
    pagination_class = OptionalPagination

    def get_queryset(self):
        matricula = self.request.query_params.get('matricula', None)
        month = self.request.query_params.get('mes', None)
        activo = self.request.query_params.get('activo', None).lower() == 'true'
        
        if month is not None:
            queryset =  self.queryset.filter(Q(fecha_vencimiento__month=month) | Q(fecha_vencimiento__month__lt=month), id_venta__id_matricula=matricula, es_activo=activo)
            return queryset        
        queryset = self.queryset.filter(id_venta__id_matricula=matricula, es_activo=activo)
        return queryset

class PagoVentaDetailView(generics.RetrieveUpdateAPIView):
    queryset = PagoVenta.objects.all()
    serializer_class = serializer.PagoVentaOutputSerializer

# ---------------------------------------------
# -----------vistas de Compras------------------
# ---------------------------------------------

class CompraListCreateView(generics.ListCreateAPIView):
    queryset = Compra.objects.all()
    serializer_class = serializer.CompraInputSerializer
    pagination_class = OptionalPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter] 
    search_fields = []

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializer.CompraOutputSerializer
        else:
            return self.serializer_class

    def create(self, request, *args, **kwargs):
         
        compra = request.data.get('compra')
        compraSerializer = self.get_serializer(data=compra)
        compraSerializer.is_valid(raise_exception=True)

        detalleList = request.data.get('detalle', [])

        if not detalleList:
            return Response({'error':'No se encontro detalle de compra'}, status=status.HTTP_404_NOT_FOUND)
        for detalle in detalleList:
            detalleSerializer =  serializer.DetalleCompraInputSerializer(data=detalle);
            detalleSerializer.is_valid(raise_exception=True)
            producto = Producto.objects.get(pk=detalle['id_producto']);
            cantidad = detalle['cantidad']
            if cantidad < 1:
                return Response({'error':'Cantidad insuficiente'}, status=status.HTTP_400_BAD_REQUEST)

        id_flujoCaja = compra['id_flujoCaja'] or None
 
        if id_flujoCaja: 
            flujoCaja = FlujoCaja.objects.get(pk=id_flujoCaja)
            if flujoCaja.monto_flujoCaja < compra['monto']:
                return Response({'error':'No hay suficiente saldo en la caja'}, status=status.HTTP_412_PRECONDITION_FAILED)
            else:                
                flujoCaja.monto_flujoCaja -= compra['monto']
                flujoCaja.salida += compra['monto']
                flujoCaja.save()
                pass

        compra = compraSerializer.save() 

        for detalle in detalleList:
            detalleSerializer =  serializer.DetalleCompraInputSerializer(data=detalle);
            detalleSerializer.is_valid(raise_exception=True)
            detalleSerializer.validated_data['id_compra'] = compra 
            detalleSerializer.save()
            producto = Producto.objects.get(pk=detalle['id_producto']);
            producto.stock += detalle['cantidad']
            producto.save()
        
        return Response(compraSerializer.data, status=status.HTTP_201_CREATED)

class CompraDetailView(generics.RetrieveUpdateAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaInputSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializer.VentaOutputSerializer
        else:
            return self.serializer_class


# ---------------------------------------------
# -----------vistas de Flujo de Caja------------------
# ---------------------------------------------

class FlujoCajaListCreateView(generics.ListCreateAPIView):
    queryset = FlujoCaja.objects.all()
    pagination_class = OptionalPagination
    serializer_class = serializer.FlujoCajaOutputSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter] 
    filterset_fields = ['fecha']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializer.FlujoCajaNormalSerializer
        else:
            return serializer.FlujoCajaInputSerializer
    
    def get(self, request, *args, **kwargs):
        current =  request.query_params.get('current', None)
        if current is not None:
            current = current.lower() == 'true'
            if current:
                try:
                    obj = FlujoCaja.get_current()
                    if obj:
                        serializer = self.serializer_class(obj)
                        return Response(serializer.data)
                    else:
                        return Response({'is_active': False,'error': 'No hay flujo de caja activo'}, status=status.HTTP_404_NOT_FOUND)
                except Exception as e:
                    return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                try:
                    obj = FlujoCaja.get_current()
                    if obj and obj.es_activo==True:
                        serializer = self.get_serializer(obj)
                        return Response(serializer.data)
                    else:
                        return Response({'is_active': False,'error': 'No hay flujo de caja activo'}, status=status.HTTP_404_NOT_FOUND)
                except Exception as e:
                    return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        return super().get(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
 
class FlujoCajaDetailView(generics.RetrieveUpdateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = FlujoCaja.objects.all()
    serializer_class = serializer.FlujoCajaOutputSerializer
            
    def update(self, request, *args, **kwargs):
        flujoCaja = self.get_object()
        serializer = self.get_serializer(flujoCaja, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        try:
            serializer.save()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().update(request, *  args, **kwargs)

# ---------------------------------------------
# -----------vistas de Tipo Actividad-------------
# ---------------------------------------------

from .models import Actividad, TipoActividad, PagoActividad
from .serializer import ActividadOutputDetailSerializer, ActividadInputSerializer, ActividadOutputSerializer, TipoActividadSerializer, PagoActividadInputSerializer, PagoActividadOutputSerializer
from academico.models import Periodo, Matricula
from django.db.models import Sum

class TipoActividadListCreateView(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = TipoActividad.objects.all()
    pagination_class = OptionalPagination
    serializer_class = TipoActividadSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]  
    search_fields = ['nombre']

class TipoActividadDetailView(generics.RetrieveUpdateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = TipoActividad.objects.all()
    serializer_class = TipoActividadSerializer
    
# ---------------------------------------------
# -----------vistas de actividades-------------
# ---------------------------------------------

class ActividadListCreateView(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Actividad.objects.all().order_by('-fecha', 'es_activo')
    pagination_class = OptionalPagination
    # serializer_class = serializer.FlujoCajaOutputSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter] 
    filterset_fields = ['id_grado', 'id_periodo']
    search_fields = ['id_tipoActividad__nombre']
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ActividadOutputSerializer
        else:
            return ActividadInputSerializer
    
    def get_queryset(self):
        id_periodo = self.request.query_params.get('id_periodo', None)
        if not id_periodo:
            periodo = Periodo.get_current()
            if not periodo:
                return Actividad.objects.none()
            queryset =  self.queryset.filter(id_periodo=periodo.id_periodo)
            return queryset
        return self.queryset
    
        
    def create(self, request, *args, **kwargs):
        data = request.data
        periodo = Periodo.get_current()
        if not periodo:
            return Response({"error": "No hay un período académico activo"}, status=status.HTTP_404_NOT_FOUND)
        for dt in data:
            serializer = self.get_serializer(data=dt)
            serializer.is_valid(raise_exception=True)
            dt['id_periodo']=periodo.id_periodo
        serializerGroup = self.get_serializer(data=data, many=True)
        if serializerGroup.is_valid():
            serializerGroup.save()
            return Response(serializerGroup.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActividadDetailView(generics.RetrieveUpdateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Actividad.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ActividadOutputDetailSerializer
        else:
            return ActividadInputSerializer
    
    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
            
# ---------------------------------------------
# -----------vistas de Pago Actividades-------------
# ---------------------------------------------
def get_pago_pendiente(id_matricula): 
        try:
            matricula = Matricula.objects.get(pk=id_matricula)
        except:
            return []
        periodo = Periodo.get_current()
        if periodo is None:
            return Response({"error": "No hay un período académico activo"}, status=status.HTTP_404_NOT_FOUND)
        actividades = Actividad.objects.filter(id_grado=matricula.id_grado, id_periodo=periodo.id_periodo, es_activo=True) 
        actividades_serialized = ActividadInputSerializer(data=actividades, many=True)
        actividades_serialized.is_valid()
        if not actividades_serialized:
            return Response([], status=status.HTTP_204_NO_CONTENT)
        pagosActividad = []
        for actividad in actividades:
            pago = {
                'id_matricula': matricula.id_matricula,
                'alumno': matricula.id_alumno.__str__(),
                'id_actividad': actividad.id_actividad,
                'actividad': actividad.id_tipoActividad.nombre,
                'fecha': actividad.fecha,
                'monto': 0
            }
            pagos = PagoActividad.objects.filter(id_actividad=actividad.id_actividad, id_matricula=id_matricula)
            total_pagado = pagos.aggregate(total_pagado=Sum('monto'))['total_pagado'] or 0
            monto = actividad.monto - total_pagado
            if monto > 0:
                pago['monto'] = monto
                pagosActividad.append(pago)
        return pagosActividad
    
class PendientePagoActividadView(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)
     def get(self, request, *args, **kwargs):
        id_matricula = self.request.query_params.get('id_matricula') or None
        if id_matricula is None:
            return Response({"error": "no se entro el parametro id_matricula"}, status=status.HTTP_404_NOT_FOUND)
        try:
            matricula = Matricula.objects.get(pk=id_matricula)
        except:
            return Response({"error": "No se encontro la matricula"}, status=status.HTTP_404_NOT_FOUND)
        return Response(get_pago_pendiente(id_matricula=id_matricula))
    

class PagoActividadListView(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = PagoActividad.objects.all()
    pagination_class = OptionalPagination
    # serializer_class = serializer.FlujoCajaOutputSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter] 
    filterset_fields = ['id_actividad', 'id_matricula']
    search_fields = ['^id_actividad__id_tipoActividad__nombre']
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PagoActividadOutputSerializer
        else:
            return PagoActividadInputSerializer
                                 
class PagoActividadDetailView(generics.RetrieveUpdateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = TipoActividad.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PagoActividadOutputSerializer
        else:
            return PagoActividadInputSerializer

#----------------------------
#---vista EstadoDeCuenta-----
#---------------------------- 

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def EstadoDeCuenta(request, pk):    
    try:
        matricula = Matricula.objects.get(id_matricula=pk)
    except Matricula.DoesNotExist:
         return Response({"error": "No se encontro la matricula"}, status=status.HTTP_404_NOT_FOUND)
        
    actividad_pagos = PagoActividad.objects.filter(id_matricula=matricula)
    actividad_pagosSerializer = PagoActividadOutputSerializer(data=actividad_pagos, many=True) 
    actividad_pagosSerializer.is_valid()
    
    actividad_pendiente = get_pago_pendiente(id_matricula=pk) 
    
    aranceles = Arancel.objects.filter(id_matricula=pk)
    aranceles_serialized = ArancelOutputSerializer(data=aranceles, many=True)
    aranceles_serialized.is_valid()
    
    pago_ventas = PagoVenta.objects.filter(id_venta__id_matricula=pk).order_by('id_venta')
    ventas_serialized = serializer.PagoVentaOutputSerializer(data=pago_ventas, many=True)
    ventas_serialized.is_valid()
    
    return Response({'actividad_pagos': actividad_pagosSerializer.data, 
                     'actividad_pendiente': actividad_pendiente, 
                     'aranceles':aranceles_serialized.data,
                     'ventas':ventas_serialized.data})

class FormaPagoListCreateView(generics.ListCreateAPIView):
    queryset = FormaPago.objects.all()
    serializer_class = serializer.FormaPagoSerializer
    pagination_class = OptionalPagination
    # permission_classes = (IsAuthenticated,)

class FormaPagoDetailView(generics.RetrieveUpdateAPIView):
    queryset = FormaPago.objects.all()
    serializer_class = serializer.FormaPagoSerializer
    # permission_classes = (IsAuthenticated,)


from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from basics.email_config import send_email

class FileUploadView(APIView):
    parser_class = (MultiPartParser, FormParser) 
    
    def post(self, request, format=None):
        file_obj = request.FILES.get('pdf_file')
        email = request.POST.get('email')

        if email and file_obj:
            subject = 'PDF File Attachment'
            message = 'Please find the attached PDF file.'

            # Create the email message with attachment
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = 'your_from_email@example.com'
            msg['To'] = email

            # Attach the PDF file
            attachment = MIMEApplication(file_obj.read())
            attachment['Content-Disposition'] = f'attachment; filename={file_obj.name}'
            msg.attach(attachment)

            # Add the message body
            msg.attach(MIMEText(message))

            # Send the email using the send_email method
            send_email(subject, msg.as_string(), email)

            return Response('Email sent successfully!')
        else:
            return Response('Invalid request. Please provide an email and a PDF file.')

#-------
#-------
#-------    
#-------
# reports
#-------
#-------
#-------
from django.db.models import Sum, Count, Q, F
from django.views import View
from django.http import JsonResponse
from .models import Producto, DetalleVenta

class ProductCountsView(View):
    # permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        # Total products sold
        total_sold = DetalleVenta.objects.aggregate(total_sold=Sum('cantidad'))['total_sold']

        # Total amount of products, active, inactive and total
        product_counts = Producto.objects.aggregate(
            total=Count('id_producto', filter=Q(tipo="PR")),
            active=Count('id_producto', filter=Q(tipo="PR", es_activo=True)),
            inactive=Count('id_producto', filter=Q(tipo="PR", es_activo=False))
        )

        # Amount of products below minimum level (stock_minimo)
        low_stock = Producto.objects.filter(tipo="PR", stock__lt=F('stock_minimo')).count()

        # Amount of products out of stock
        out_of_stock = Producto.objects.filter(stock=0, tipo="PR").count()

        data = {
            'total_sold': total_sold,
            'total_products': product_counts['total'],
            'active_products': product_counts['active'],
            'inactive_products': product_counts['inactive'],
            'low_stock': low_stock,
            'out_of_stock': out_of_stock
        }

        return JsonResponse(data)
    
class CashFlowCountsView(View):
    # permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        # Total global entrada
        total_entrada = FlujoCaja.objects.aggregate(total_entrada=Sum('entrada'))['total_entrada'] or 0

        # Total global salida
        total_salida = FlujoCaja.objects.aggregate(total_salida=Sum('salida'))['total_salida'] or 0

        # Total global balance
        balance_total = total_entrada - total_salida
        
         # Total amount of payments (monto)
        total_pago_actividad = PagoActividad.objects.aggregate(total_pago=Sum('monto'))['total_pago'] or 0

        # Total amount of payments (monto) from PagoVenta
        total_pago_venta = PagoVenta.objects.filter(es_activo=False, id_comprobante__isnull=False).aggregate(total_pago=Sum('monto'))['total_pago'] or 0

        # Total amount of payments (monto) from Arancel
        total_pago_arancel = Arancel.objects.filter(es_activo=False, id_comprobante__isnull=False).aggregate(total_pago=Sum('monto'))['total_pago'] or 0

        # Total amount of descuentos from DescuentoBeca
        total_descuento_beca = DescuentoBeca.objects.aggregate(total_descuento=Sum('monto'))['total_descuento'] or 0

       # Total amount of comprobantes (monto) registered
        total_monto_comprobantes = Comprobante.objects.aggregate(total_monto=Sum('monto'))['total_monto'] or 0
        
        # Total amount of comprobantes registered
        total_comprobantes = Comprobante.objects.count()

         # Total amount of comprobantes (monto) by forma de pago
        forma_pago_summary = Comprobante.objects.values('id_formaPago__nombre').annotate(
            cantidad=Count('id_comprobante'),
            total_monto=Sum('monto')
        )

        forma_pago_data = {}
        for forma_pago in forma_pago_summary:
            forma_pago_data[f"cantidad_{forma_pago['id_formaPago__nombre']}"] = forma_pago['cantidad']
            forma_pago_data[f"total_{forma_pago['id_formaPago__nombre']}"] = forma_pago['total_monto']

        data = {
            'total_global_entrada': total_entrada,
            'total_global_salida': total_salida,
            'total_global_balance': balance_total,
            'total_pago_actividad': total_pago_actividad,
            'total_pago_venta': total_pago_venta,
            'total_pago_arancel': total_pago_arancel,
            'total_descuento_beca': total_descuento_beca,
            'total_comprobantes': total_comprobantes,
            'total_monto_comprobantes': total_monto_comprobantes,
            **forma_pago_data
        }

        return JsonResponse(data)
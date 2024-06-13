from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from .models import Producto, Arancel, Timbrado, Comprobante, PagoVenta, Venta, DetalleVenta
from .serializer import ComprobanteSerializer,  ProductoSerializer, ArancelInputSerializer, ArancelOutputSerializer, TimbradoSerializer, VentaInputSerializer, DetalleVentaSerializer, PagoVentaInputSerializer 
from . import serializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from academico.views import OptionalPagination
from django.db.models import Q
# ---------------------------------------------
# ---------vistas de productos-----------------
# ---------------------------------------------

class ProductoListCreateView(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    pagination_class = OptionalPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter] 
    search_fields = ['^nombre','^descripcion']
    filterset_fields = ['tipo', 'grados']

class ProductoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

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
    serializer_class = ComprobanteSerializer

    def create(self, request, *args, **kwargs):
        comprobante = request.data.get('comprobante')
        serializer = self.get_serializer(data=comprobante)
        serializer.is_valid(raise_exception=True)
        id_timbrado = comprobante.get('id_timbrado');

        if id_timbrado: 
            timbrado = Timbrado.objects.get(pk=id_timbrado)
            if not timbrado.es_activo:
                return Response({'error': 'El timbrado no esta activo'}, status=status.HTTP_400_BAD_REQUEST) 
            if timbrado.ultimo_numero == 0:
                serializer.validated_data['nro_factura'] = timbrado.ultimo_numero = timbrado.numero_inicial
            else:
                serializer.validated_data['nro_factura'] = timbrado.ultimo_numero = timbrado.ultimo_numero + 1
            timbrado.save()

        aranceles = request.data.get('aranceles',[])
        pagoventas = request.data.get('pagoventas',[])
        actividades = request.data.get('actividades', []) 

        if not aranceles and not pagoventas and not actividades:
            return Response({'error':'No se encontradon pagos'}, status=status.HTTP_404_NOT_FOUND)
        
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
                payment = Arancel.objects.get(pk=arancel)
                # payment.id_comprobante = invoice 
                # payment.es_activo = False
                # payment.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ComprobanteDetailView(generics.RetrieveUpdateAPIView):
    queryset = Comprobante.objects.all()
    serializer_class = ComprobanteSerializer

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
        """
        Override create method to handle list of payments
        """
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
            
    # def update(self, request, *args, **kwargs):
    #         partial = kwargs.pop('partial', False)
    #         instance = self.get_object()
    #         serializer = self.get_serializer(instance, data=request.data, many=True, partial=partial)
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_update(serializer)

    #         return Response(serializer.data)

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
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

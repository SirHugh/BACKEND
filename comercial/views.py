from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, filters
from .models import ControlStock, DetalleControl
from .serializers import ControlStockSerializer, DetalleControlSerializer 
from django_filters.rest_framework import DjangoFilterBackend
from academico.views import OptionalPagination
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, DjangoObjectPermissions
from caja.views import ProductoListCreateView
from django.db.models import Q
from caja.models import Producto

# Create your views here.
class ControlListView(generics.ListAPIView):
    queryset = ControlStock.objects.all()
    serializer_class = ControlStockSerializer
    pagination_class = OptionalPagination
    # permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter] 
    # search_fields = ['nombre','descripcion']
    # filterset_fields = ['tipo', 'grados','es_activo']
   
class InitiateStockControlView(ProductoListCreateView):
    
    def create(self, request, *args, **kwargs):
        # Get the filtering parameters from the request
        filters = request.query_params.get('filters', {})
        search_query = request.query_params.get('search', '')

        # Get the filtered products using the same filtering logic as the list view
        filtered_products = self.filter_queryset(self.get_queryset())
        filtered_products = filtered_products.filter(**filters)
        if search_query:
            filtered_products = filtered_products.filter(Q(nombre__icontains=search_query) | Q(descripcion__icontains=search_query))
 
        # Crea una nueva entrada ControlStock
        control_stock = ControlStock.objects.create(id_usuario=request.user, cantidad_productos=filtered_products.count())

        # Crea DetalleControl entradas para cada producto filtrado
        detalle_controls = []
        for product in filtered_products:
            detalle_control = DetalleControl(
                id_controlStock=control_stock,
                id_producto=product,
                stock=product.stock,
                cantidad_contada=0  # Inicializa la cantidad_contada a 0
            )
            detalle_controls.append(detalle_control)

        DetalleControl.objects.bulk_create(detalle_controls)

        # Rertona la entada ControlStock creada
        serializer = ControlStockSerializer(control_stock)
        return Response(serializer.data)
    

class ControlDatailView(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = ControlStock.objects.all()
    serializer_class = ControlStockSerializer 

class CloseStockControlView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = ControlStock.objects.all()
    serializer_class = ControlStockSerializer 
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.es_activo = False
        detalle_control = DetalleControl.objects.filter(id_controlStock=instance)
        for detalle in detalle_control:
            diferencia = detalle.cantidad_contada - detalle.stock
            producto = Producto.objects.get(pk=detalle.id_producto.id_producto)
            producto.stock += diferencia;
            print(producto, detalle.stock, detalle.cantidad_contada, diferencia, producto.stock)
            producto.save()
        instance.save()
        return super().get(request, *args, **kwargs)
 
class DetalleControlListView(generics.ListAPIView):
    queryset = DetalleControl.objects.all()
    serializer_class = DetalleControlSerializer
    pagination_class = OptionalPagination 
    # permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter] 
    search_fields = ['id_producto__nombre', 'id_producto__descripcion']
    filterset_fields = ['id_controlStock']
    
class DetalleControlDetailView(generics.RetrieveUpdateAPIView):
    queryset = DetalleControl.objects.all()
    serializer_class = DetalleControlSerializer
    # permission_classes = [IsAuthenticated, DjangoModelPermissions]
    
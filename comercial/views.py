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

        print("","\nproductos filtrados")
        print(filtered_products)
        print("","\nproductos filtrados")
        # Crea una nueva entrada ControlStock
        control_stock = ControlStock.objects.create(id_usuario=request.user)

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
    queryset = ControlStock.objects.all()
    serializer_class = ControlStockSerializer
    pagination_class = OptionalPagination
    # permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter] 
 
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
    
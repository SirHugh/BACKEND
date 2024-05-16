from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from .models import Producto, Arancel, Timbrado, Factura, Comprobante, Recibo
from .serializer import ComprobanteSerializer, ReciboSerializer, ProductoSerializer, ArancelInputSerializer, ArancelOutputSerializer, TimbradoSerializer, FacturaSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from academico.views import OptionalPagination

# ------------------------- vistas de productos -----------------------------.
class ProductoListCreateView(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    pagination_class = OptionalPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter] 
    search_fields = ['^nombre']
    filterset_fields = ['tipo', 'grados']

class ProductoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


# ------------------------- vistas de Timbrado -----------------------------.
class TimbradoListCreateView(generics.ListCreateAPIView):
    queryset = Timbrado.objects.all()
    serializer_class = TimbradoSerializer

class TimbradoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Timbrado.objects.all()
    serializer_class = TimbradoSerializer
    
# ------------------------- vistas de Factura -----------------------------.
class FacturaListCreateView(generics.ListCreateAPIView):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer

class FacturaDetailView(generics.RetrieveUpdateAPIView):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer

# ------------------------- vistas de Comprobante -----------------------------.
class ComprobanteListCreateView(generics.ListCreateAPIView):
    queryset = Comprobante.objects.all()
    serializer_class = ComprobanteSerializer

class ComprobanteDetailView(generics.RetrieveUpdateAPIView):
    queryset = Comprobante.objects.all()
    serializer_class = ComprobanteSerializer

# ------------------------- vistas de arancel -----------------------------.
class ArancelListCreateView(generics.ListCreateAPIView):
    queryset = Arancel.objects.all()
    serializer_class = ArancelInputSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter] 
    search_fields = ['=id_matricula__id_alumno__cedula', '^id_matricula__id_alumno__nombre', '^id_matricula__id_alumno__apellido']
    filterset_fields = ['es_activo', 'id_comprobante']
     
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


class ArancelDetailView(generics.RetrieveUpdateAPIView):
    queryset = Arancel.objects.all()
    serializer_class = ArancelInputSerializer

    def get_serializer_class(self):
            if self.request.method == 'GET':
                return ArancelOutputSerializer
            else:
                return self.serializer_class





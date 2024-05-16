from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, permission_classes 
from rest_framework.response import Response
from .models import Alumno, Grado, Matricula, Beca, Becado, Cliente, Responsable
from .serializer import AlumnoInputSerializer, AlumnoOutputSerializer, GradoSerializer, MatriculaInputSerializer, MatriculaOutputSerializer, BecaSerializer, BecadoInputSerializer, BecadoOutputSerializer, ClienteSerializer, ResponsableInputSerializer, ResponsableOutputSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, DjangoObjectPermissions
from rest_framework import filters 
from django_filters.rest_framework import DjangoFilterBackend
import math 

class OptionalPagination(PageNumberPagination):
    
    def paginate_queryset(self, queryset, request, view=None):
        page = request.query_params.get('page') 
        if page:
            return super().paginate_queryset(queryset, request, view=view)
        return None

#-------------Vista de grado----------------------------------
class GradoListCreateView(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Grado.objects.all()
    pagination_class = None
    serializer_class = GradoSerializer
    
class GradoDetailView(generics.RetrieveUpdateAPIView): 
    # permission_classes = (IsAuthenticated,)
    queryset = Grado.objects.all()
    serializer_class = GradoSerializer

#-------------Vista de alumno----------------------------------
class AlumnoListCreateView(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Alumno.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = OptionalPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['cedula']
    search_fields = ['^cedula', '^nombre', '^apellido']

    def get_serializer_class(self):
        if self.request.method == 'POST' or  self.request.method == "PUT" or  self.request.method == "PATCH":
            return AlumnoInputSerializer
        return AlumnoOutputSerializer  


class AlumnoDetailView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Alumno.objects.all()
    serializer_class = AlumnoInputSerializer


#------------------------------Vistas de Matriculas-------------------------------
class MatriculaListCreateView(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Matricula.objects.all().order_by('-fecha_inscripcion' )
    pagination_class = OptionalPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id_grado', 'anio_lectivo', 'es_activo', 'id_alumno__cedula']
    search_fields = ['^id_alumno__apellido', 'id_alumno__nombre','=id_alumno__cedula','^id_grado__grado',  ]

    def get_serializer_class(self):
        if self.request.method == 'POST' or  self.request.method == "PUT" or  self.request.method == "PATCH":
            return MatriculaInputSerializer
        return MatriculaOutputSerializer 
     
class MatriculaDetailView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Matricula.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST' or  self.request.method == "PUT" or  self.request.method == "PATCH":
            return MatriculaInputSerializer
        return MatriculaOutputSerializer 

# ---------------------------------vistas de becas-----------------------
class BecaListCreateView(generics.ListCreateAPIView):
    queryset = Beca.objects.all().order_by("-es_activo")
    serializer_class = BecaSerializer
    pagination_class = None

class BecaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Beca.objects.all()
    serializer_class = BecaSerializer

# ---------------------------------vistas de becados----------------------
class becadoListCreateView(generics.ListCreateAPIView):
    queryset = Becado.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = PageNumberPagination
    filterset_fields = ['id_beca', 'id_matricula']
    search_fields = ['^id_matricula__id_alumno__apellido', '^id_matricula__id_alumno__nombre', '^id_matricula__id_alumno__cedula' ]

    
    def get_serializer_class(self):
        if self.request.method == 'POST'or  self.request.method == "PUT" or  self.request.method == "PATCH":
            return BecadoInputSerializer
        return BecadoOutputSerializer 

class BecadoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Becado.objects.all()
        
    def get_serializer_class(self):
        if self.request.method == 'POST'or  self.request.method == "PUT" or  self.request.method == "PATCH":
            return BecadoInputSerializer
        return BecadoOutputSerializer 

  
@api_view(['GET', 'PUT', 'DELETE'])
def becado_detail(request, pk):
    """
    Obtener, actualizar o eliminar una matriculacion. 
    """
    try:
        becado = Becado.objects.filter(id_beca=pk)
    except becado.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BecadoOutputSerializer(becado, many=True)
        return Response(serializer.data)
 

#------------------vistas de clientes----------------------------------
class ClienteListCreateView(generics.ListCreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer 
    pagination_class = OptionalPagination 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['cedula']

class ClienteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

#-------------Vistas de Responsables----------------------------------
class ResponsableListCreateView(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Responsable.objects.all() 
    pagination_class = None
    filter_backends = [DjangoFilterBackend, filters.SearchFilter] 
    search_fields = ['^cliente__cedula', '^cliente__nombre', '^cliente__apellido']

    def get_serializer_class(self):
        if self.request.method == 'POST' or  self.request.method == "PUT" or  self.request.method == "PATCH":
            return ResponsableInputSerializer
        return ResponsableOutputSerializer  

class ResponsableVerifyView(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Responsable.objects.all() 
    serializer_class = ResponsableInputSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id_cliente', 'id_alumno']

class ResponsableDetailView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Responsable.objects.all() 

    def get_serializer_class(self):
        if self.request.method == 'POST' or  self.request.method == "PUT" or  self.request.method == "PATCH":
            return ResponsableInputSerializer
        return ResponsableOutputSerializer 

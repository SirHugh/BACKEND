from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from .models import Alumno, Grado, Matricula, Beca, Becado, Cliente, Responsable, Periodo
from .serializer import BecaMatriculaSerializer, AlumnoInputSerializer, AlumnoOutputSerializer, GradoSerializer, PeriodoSerializer, MatriculaInputSerializer, MatriculaOutputSerializer, BecaSerializer, BecadoInputSerializer, BecadoOutputSerializer, ClienteSerializer, ResponsableInputSerializer, ResponsableOutputSerializer
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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['es_activo']
    
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
    search_fields = ['^cedula', 'nombre', 'apellido']

    def get_serializer_class(self):
        if self.request.method == 'POST' or  self.request.method == "PUT" or  self.request.method == "PATCH":
            return AlumnoInputSerializer
        return AlumnoOutputSerializer  


class AlumnoDetailView(generics.RetrieveUpdateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Alumno.objects.all()
    serializer_class = AlumnoInputSerializer

#------------------------------Vistas de Matriculas-------------------------------
class MatriculaListCreateView(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Matricula.objects.all().order_by('es_activo','-fecha_inscripcion' )
    pagination_class = OptionalPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id_grado', 'anio_lectivo', 'es_activo', 'id_alumno__cedula', 'id_alumno']
    search_fields = ['id_alumno__apellido', 'id_alumno__nombre','^id_alumno__cedula','^id_grado__grado',  ]

    def get_serializer_class(self):
        if self.request.method == 'POST' or  self.request.method == "PUT" or  self.request.method == "PATCH":
            return MatriculaInputSerializer
        return MatriculaOutputSerializer 

class ResponsalbeMatriculaListView(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = MatriculaOutputSerializer
    pagination_class = None  
     
    def get_queryset(self):
        responsable_intances = Responsable.objects.filter(id_cliente=self.kwargs['pk'])
        queryset = Matricula.objects.filter(id_alumno__in=responsable_intances.values_list('id_alumno', flat=True), es_activo=True)
        return queryset

class MatriculaDetailView(generics.RetrieveUpdateAPIView):
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

class BecaDetailView(generics.RetrieveUpdateAPIView):
    queryset = Beca.objects.all()
    serializer_class = BecaSerializer

# ---------------------------------vistas de becados----------------------
class becadoListCreateView(generics.ListCreateAPIView):
    queryset = Becado.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = OptionalPagination
    filterset_fields = ['id_beca', 'id_matricula', 'es_activo']
    search_fields = ['^id_matricula__id_alumno__apellido', '^id_matricula__id_alumno__nombre', '^id_matricula__id_alumno__cedula' ]

    
    def get_serializer_class(self):
        if self.request.method == 'POST'or  self.request.method == "PUT" or  self.request.method == "PATCH":
            return BecadoInputSerializer
        return BecadoOutputSerializer 

class BecadoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Becado.objects.all()
        
    def get_serializer_class(self):
        if self.request.method == 'POST'or  self.request.method == "PUT" or  self.request.method == "PATCH":
            return BecadoInputSerializer
        return BecadoOutputSerializer 

  
@api_view(['GET'])
def becado_detail(request, pk):
    """
    Obtener, actualizar o eliminar una matriculacion. 
    """
    try:
        becado = Becado.objects.filter(id_matricula=pk, es_activo=True)
    except becado.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BecaMatriculaSerializer(becado, many=True)
        return Response(serializer.data)

#------------------vistas de clientes----------------------------------
class ClienteListCreateView(generics.ListCreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer 
    pagination_class = OptionalPagination 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['cedula']
    search_fields = ['cedula', 'nombre', 'apellido']

class ClienteDetailView(generics.RetrieveUpdateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

#-------------Vistas de Responsables----------------------------------
class ResponsableListCreateView(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Responsable.objects.all() 
    pagination_class = OptionalPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter] 
    search_fields = ['^id_cliente__cedula', '^id_cliente__nombre', '^id_cliente__apellido']

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

class ResponsableDetailView(generics.RetrieveUpdateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Responsable.objects.all() 

    def get_serializer_class(self):
        if self.request.method == 'POST' or  self.request.method == "PUT" or  self.request.method == "PATCH":
            return ResponsableInputSerializer
        return ResponsableOutputSerializer 

#--------------------------------Periodo Views ---------------------------

class PeriodoListCreateView(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Periodo.objects.all() 
    pagination_class = OptionalPagination
    serializer_class = PeriodoSerializer
    filter_backends = [DjangoFilterBackend] 
    filterset_fields = ['es_activo']


class PeriodoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Periodo.objects.all()
    serializer_class = PeriodoSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if Periodo.objects.filter(es_activo=True).exclude(pk=instance.pk).exists():
            return Response({'error': 'Ya existe un periodo activo'}, status=status.HTTP_400_BAD_REQUEST)

        if not instance.es_activo and serializer.validated_data['es_activo']:
            instance.es_activo = True
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        return super().update(request, *args, **kwargs)
    

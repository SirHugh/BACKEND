from rest_framework import status, generics
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from .models import Alumno, Grado, Matricula, Beca, Becado, Cliente, Responsable
from .serializer import AlumnoInputSerializer, AlumnoOutputSerializer, GradoSerializer, MatriculaInputSerializer, MatriculaOutputSerializer, BecaSerializer, BecadoSerializer, ClienteSerializer, ResponsableInputSerializer, ResponsableOutputSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
import math 

# vista de alumnos.

@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def alumno_list(request):

    if request.method == 'GET':
        PAGE_SIZE = 10;
        
        # Retrieve the items from the database
        alumnos = Alumno.objects.all()
        
        # Create a paginator with the desired number of items per page
        paginator = PageNumberPagination()
        paginator.page_size = PAGE_SIZE;  # Change this value to set the number of items per page
        result_page = paginator.paginate_queryset(alumnos, request)
        serializer = AlumnoOutputSerializer(result_page, many=True, context={"request": request})
        # Return the paginated items as a response
        number_of_pages = math.ceil(alumnos.count() / PAGE_SIZE);
        # number_of_pages = int(number_of_pages) if number_of_pages.is_integer() else math.ceil(number_of_pages)

        return Response({'data': serializer.data, 'number_of_pages': number_of_pages } )
        

    elif request.method == 'POST':
        serializer = AlumnoInputSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser, FormParser])
def alumno_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        alumno = Alumno.objects.get(pk=pk)
    except alumno.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AlumnoInputSerializer(alumno, context={"request": request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AlumnoInputSerializer(alumno, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        alumno.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#vista de grados
    
@api_view(['GET', 'POST'])
def grado_list(request):
    """
    Crear un grado o listar los grados
    """
    if request.method == 'GET':
        grados = Grado.objects.all()
        serializer = GradoSerializer(grados, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = GradoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def grado_detail(request, pk):
    """
    Obtener, Actualizar o eliminar un grado.
    """
    try:
        grado = Grado.objects.get(pk=pk)
    except grado.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GradoSerializer(grado)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GradoSerializer(grado, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        grado.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#-------------------vistas de la clase Matriculas---------------------------
    
@api_view(['GET', 'POST'])
def matricula_list(request):
    """
    Lista las matriculaciones o registra una matriculacion.
    """
    if request.method == 'GET':
        matricula = Matricula.objects.all()
        serializer = MatriculaOutputSerializer(matricula, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MatriculaInputSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def matricula_detail(request, pk):
    """
    Obtener, actualizar o eliminar una matriculacion. 
    """
    try:
        matricula = Matricula.objects.get(pk=pk)
    except matricula.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MatriculaOutputSerializer(matricula)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MatriculaInputSerializer(matricula, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        matricula.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

#-------------------vistas de la clase Beca---------------------------
    
@api_view(['GET', 'POST'])
def beca_list(request):
    """
    Lista las matriculaciones o registra una matriculacion.
    """
    if request.method == 'GET':
        beca = Beca.objects.all()
        serializer = BecaSerializer(beca, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BecaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def beca_detail(request, pk):
    """
    Obtener, actualizar o eliminar una matriculacion. 
    """
    try:
        beca = Beca.objects.get(pk=pk)
    except beca.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BecaSerializer(beca)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BecaSerializer(beca, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        beca.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#-------------------vistas de la clase becado---------------------------
    
@api_view(['GET', 'POST'])
def becado_list(request):
    """
    Lista las matriculaciones o registra una matriculacion.
    """
    if request.method == 'GET':
        becado = Becado.objects.all()
        serializer = BecadoSerializer(becado, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BecadoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
        serializer = BecadoSerializer(becado, many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BecadoSerializer(becado, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        becado.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class becadoListCreateView(generics.ListCreateAPIView):
    queryset = Becado.objects.all()
    serializer_class = BecadoSerializer

class BecadoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Becado.objects.all()
    serializer_class = BecadoSerializer

class ClienteListCreateView(generics.ListCreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ClienteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ClienteListCreateView(generics.ListCreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


#-------------------vistas de la clase responsable---------------------------
    
@api_view(['GET', 'POST'])
def responsable_list(request):
    """
    Lista las matriculaciones o registra una matriculacion.
    """
    if request.method == 'GET':
        responsable = Responsable.objects.all()
        serializer = ResponsableOutputSerializer(responsable, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ResponsableInputSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def responsable_detail(request, pk):
    """
    Obtener, actualizar o eliminar una matriculacion. 
    """
    try:
        responsable = Responsable.objects.filter(cliente=pk)
    except responsable.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ResponsableOutputSerializer(responsable, many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        responsable = Responsable.objects.get(pk=pk)
        serializer = ResponsableInputSerializer(responsable, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        responsable.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

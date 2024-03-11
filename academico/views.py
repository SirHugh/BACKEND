from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Alumno, Grado, Matricula
from .serializer import AlumnoSerializer, GradoSerializer, MatriculaSerializer

# vista de alumnos.
@api_view(['GET', 'POST'])
def alumno_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        alumnos = Alumno.objects.all()
        serializer = AlumnoSerializer(alumnos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AlumnoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def alumno_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        alumno = Alumno.objects.get(pk=pk)
    except alumno.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AlumnoSerializer(alumno)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AlumnoSerializer(alumno, data=request.data)
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
    
#vista de matriculas
    
@api_view(['GET', 'POST'])
def matricula_list(request):
    """
    Lista las matriculaciones o registra una matriculacion.
    """
    if request.method == 'GET':
        matricula = Matricula.objects.all()
        serializer = MatriculaSerializer(matricula, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MatriculaSerializer(data=request.data)
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
        serializer = MatriculaSerializer(matricula)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MatriculaSerializer(matricula, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        matricula.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
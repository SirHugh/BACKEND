from rest_framework import serializers
from .models import Alumno, Grado, Matricula

class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = ['cedula', 'nombre', 'apellido', 'genero',
                'fecha_nac',
                'nacionalidad', 
                'barrio', 'edad_primer_grado',
                'curso_jardin', 'cantidad_hermanos']
        

class GradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grado
        fields = ['nombre', 'grado', 'nivel', 'turno']


class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        fields = ['id_alumno', 'id_grado', 'anio_lectivo', 'fecha_inscripcion']
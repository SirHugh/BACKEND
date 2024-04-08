from rest_framework import serializers
from .models import Alumno, Grado, Matricula, Beca, Becado, Cliente, Responsable

class AlumnoInputSerializer(serializers.ModelSerializer):
    fotocarnet = serializers.ImageField(required=False)
    class Meta:
        model = Alumno
        fields = '__all__'
        
class AlumnoOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = ['id_alumno', 'nombre', 'apellido', 'cedula', 'fecha_nac', 'telefono', 'fotocarnet']
    
    def get_photo_url(self, alumno):
        request = self.context.get('request')
        photo_url = alumno.photo.url
        return request.build_absolute_uri(photo_url)


class GradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grado
        fields = '__all__'


class MatriculaInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        fields = ['id_matricula', 'id_alumno', 'id_grado', 'anio_lectivo', 'fecha_inscripcion', 'trabaja', 'es_interno']

class MatriculaOutputSerializer(serializers.ModelSerializer):
    id_alumno=AlumnoOutputSerializer()
    class Meta:
        model = Matricula
        fields = ['id_matricula', 'id_alumno', 'id_grado', 'anio_lectivo', 'fecha_inscripcion', 'trabaja', 'es_interno']

class BecaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beca
        fields = '__all__'

class BecadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Becado
        fields = ['id', 'id_beca', 'id_matricula', 'es_activo', 'fecha_inicio']

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente 
        fields = '__all__'

class ResponsableInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsable
        fields = '__all__' 

class ResponsableOutputSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer()
    class Meta:
        model = Responsable
        fields= '__all__'
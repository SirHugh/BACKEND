from django.db import models

# Create your models here.
class Alumno(models.Model):
    id_alumno = models.AutoField(primary_key=True)
    cedula = models.IntegerField(unique= True)
    nombre = models.CharField(max_length=80)
    apellido = models.CharField(max_length=100)
    fecha_nac = models.DateField(auto_now=False, auto_now_add=False)
    telefono = models.CharField(max_length=50)
    nacionalidad = models.CharField(max_length=80)
    direccion = models.CharField(max_length=254)
    barrio = models.CharField(max_length=50)
    alergico_a = models.CharField(max_length=50)
    edad_primer_grado = models.IntegerField()
    curso_jardin = models.CharField(max_length=2)
    perfil_psicologico = models.CharField(max_length=254)
    cantidad_hermanos = models.IntegerField()

    class Meta:
        ordering = ['apellido']


class Grado(models.Model):
    id_grado =  models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    grado = models.IntegerField()
    nivel = models.CharField(max_length=100)
    turno = models.CharField(max_length=15)
    seccion = models.CharField(max_length=2)

class Matricula(models.Model):
    id_matricula = models.AutoField(primary_key=True)
    id_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, null=True, blank = False)
    id_grado = models.ForeignKey(Grado, on_delete=models.CASCADE,null=True, blank = False)
    fecha_inscripcion = models.DateField(blank=False, null=True)
    anio_lectivo = models.IntegerField(null=True)
    es_activo  = models.BooleanField(default=False)
    fecha_desmatriculacion = models.DateField(null=True)




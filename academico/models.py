from django.db import models

# Create your models here.
class Alumno(models.Model):

    OPCIONES_GENERO = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    id_alumno = models.AutoField(primary_key=True)
    cedula = models.IntegerField(unique= True)
    nombre = models.CharField(max_length=80)
    apellido = models.CharField(max_length=100)
    genero = models.CharField(max_length=1, choices=OPCIONES_GENERO, null=True)
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
    fotocarnet = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None, null=True)


    class Meta:
        ordering = ['apellido']


class Grado(models.Model):
    id_grado =  models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    grado = models.IntegerField()
    nivel = models.CharField(max_length=100)
    turno = models.CharField(max_length=15)
    seccion = models.CharField(max_length=2)
    
    class Meta: 
        ordering = ['grado']

class Matricula(models.Model):
    id_matricula = models.AutoField(primary_key=True)
    id_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, null=True, blank = False)
    id_grado = models.ForeignKey(Grado, on_delete=models.CASCADE,null=True, blank = False)
    fecha_inscripcion = models.DateField(blank=False, null=True)
    anio_lectivo = models.IntegerField(null=True)
    es_activo  = models.BooleanField(default=False)
    fecha_desmatriculacion = models.DateField(null=True)
    trabaja = models.BooleanField(null=True)
    es_interno = models.BooleanField(null=True)

class Beca(models.Model):
    id_beca = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=254)
    monto = models.IntegerField()
    porcentaje = models.IntegerField()
    es_activo = models.BooleanField()

class Becado(models.Model):
    id_beca = models.ForeignKey(Beca, on_delete=models.CASCADE)
    id_matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE)
    es_activo = models.BooleanField(default=True)
    fecha_inicio = models.DateField(auto_now=False, auto_now_add=False)
    fecha_fin = models.DateField(null=True)
    class Meta:
        unique_together = (('id_beca', 'id_matricula' ),)


class Cliente(models.Model):
    cedula = models.IntegerField(unique=True)
    ruc = models.CharField(max_length=15, blank=True, null=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    direccion = models.CharField(max_length=254)
    tipo = models.CharField(max_length=10)

class Responsable(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    ocupacion = models.CharField(max_length=254)
    tipo_relacion = models.CharField(max_length=50)
    es_activo = models.BooleanField(null=True)
    class Meta:
        unique_together = ['cliente', 'alumno']

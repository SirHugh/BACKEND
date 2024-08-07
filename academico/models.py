from django.db import models

# Create your models here.
def upload_to(instance, filename):
    return 'Fotocarnets/{filename}'.format(filename=filename)

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
    telefono = models.CharField(max_length=50, blank=True)
    nacionalidad = models.CharField(max_length=80)
    direccion = models.CharField(max_length=254, blank=True)
    barrio = models.CharField(max_length=50, blank=True)
    alergico_a = models.CharField(max_length=50, null=True, blank=True)
    edad_primer_grado = models.IntegerField(null=True, blank=True)
    curso_jardin = models.BooleanField(blank=True, null=True, default=False)
    perfil_psicologico = models.CharField(max_length=254, blank=True)
    cantidad_hermanos = models.IntegerField(blank=True, null=True)
    fotocarnet = models.ImageField(upload_to=upload_to, blank=True, null=True)

    def get_nombre(self):
            return self.nombre
        
    def get_apellido(self):
        return self.apellido 
    
    def __str__(self):
         return f"{self.nombre} {self.apellido}"
    
    def get_alumno(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        ordering = ['apellido']


class Grado(models.Model):
    id_grado =  models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    grado = models.IntegerField(blank=True)
    nivel = models.CharField(max_length=100, blank=True)
    turno = models.CharField(max_length=15, blank=True)
    seccion = models.CharField(max_length=2, blank=True, null=True)
    es_activo = models.BooleanField(default=False)
    
    class Meta: 
        ordering = ['grado' ]
    
    def __str__(self):
        if not self.grado:
            return f"{self.nombre}"
        return f"{self.grado}° - {self.nombre}"

class Periodo(models.Model):
    id_periodo = models.AutoField(primary_key=True)
    periodo = models.IntegerField(null=False, unique=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    vencimiento_pagos = models.IntegerField()
    es_activo = models.BooleanField(default=False)

    class Meta:
        ordering = ['-periodo']
        
    @classmethod
    def get_current(cls): 
        periodo = cls.objects.filter(es_activo=True).first()
        return periodo
        
    # def save(self, *args, **kwargs):
    #     if self.es_activo:
    #         try:
    #             Period.objects.exclude(pk=self.pk).get(es_activo=True)
    #         except Period.DoesNotExist:
    #             super(Period, self).save(*args, **kwargs)
    #             return
    #         else:
    #             raise IntegrityError("Solo un periodo puede encontrarse activo al mismo tiempo")
    #     else:
    #         super(Period, self).save(*args, **kwargs)

class Matricula(models.Model):
    id_matricula = models.AutoField(primary_key=True)
    id_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, null=True, blank = False)
    id_grado = models.ForeignKey(Grado, on_delete=models.CASCADE,null=True, blank = False)
    # id_periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(blank=False, null=True)
    anio_lectivo = models.IntegerField(null=True)
    es_activo  = models.BooleanField(default=False)
    fecha_desmatriculacion = models.DateField(null=True)
    trabaja = models.BooleanField(blank=True, null=True)
    es_interno = models.BooleanField(blank=True, null=True)

# from caja import Producto
class Beca(models.Model):
    TIPO_OPTIONS = [
        (1, 'PORCENTAJE'),
        (2, 'MONTO FIJO'),
    ]

    id_beca = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=254)
    monto = models.IntegerField(default=0)
    tipo_monto = models.IntegerField(choices=TIPO_OPTIONS, default=0)    
    arancel = models.ManyToManyField('caja.Producto',  related_name='beca', default=0)
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
    id_cliente = models.AutoField(primary_key=True)
    cedula = models.IntegerField(unique=True)
    ruc = models.CharField(max_length=15, blank=True, null=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=254, blank=True)
    direccion = models.CharField(max_length=254, blank=True)
    tipo = models.CharField(max_length=10)

    def __str__(self):
         return f"{self.cedula} - {self.nombre} {self.apellido}"

class Responsable(models.Model):
    id_responsable = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE )
    id_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE )
    ocupacion = models.CharField(max_length=254, blank=True)
    tipo_relacion = models.CharField(max_length=50)
    es_activo = models.BooleanField(null=True)
    class Meta:
        unique_together = ['id_cliente', 'id_alumno']



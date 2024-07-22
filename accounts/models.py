from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

def upload_to(instance, filename):
    return 'UsersPhoto/{filename}'.format(filename=filename) 

class UserManager(BaseUserManager):
    def _create_user(self, email, password, nombre, apellido, telefono, **extra_fields):
        if not email:
            raise ValueError("Debe proveer un email valido")
        if not password:
            raise ValueError('Debe proporcionar una contraseña')

        user = self.model(
            email = self.normalize_email(email),
            nombre= nombre,
            apellido = apellido,
            telefono = telefono,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, nombre, apellido, telefono, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(email, password, nombre, apellido, telefono, password, **extra_fields)

    def create_superuser(self, email, password, nombre, apellido, telefono, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(email, password, nombre, apellido, telefono, **extra_fields)



    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('El usuario debe tener un correo!')
        email = self.normalize_email(email)
        user = self.model(email=email, username=name)

        user.set_password(password)
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):
    
    
    email = models.EmailField(max_length=254, unique= True) 
    nombre = models.CharField(max_length=254)
    apellido = models.CharField(max_length=100, null=True, blank=True)
    cedula = models.IntegerField(null=True, blank=True)
    direccion = models.CharField(max_length=254, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    foto = models.ImageField(upload_to=upload_to, blank=True, null=True)
    
    is_staff = models.BooleanField(default=True) # must needed, otherwise you won't be able to loginto django-admin.
    is_active = models.BooleanField(default=True) # must needed, otherwise you won't be able to loginto django-admin.
    is_superuser = models.BooleanField(default=False) # this field we inherit from PermissionsMixin.


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'telefono'] 

    def get_nombre(self):
        return self.nombre
    
    def get_apellido(self):
        return self.apellido 
    
    def __str__(self):
        return f'{self.nombre +' '+ str(self.apellido)}'
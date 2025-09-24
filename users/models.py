from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

# Modelo para los Roles, tal como en tu script SQL.
class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

# Un "Manager" para nuestro modelo de Usuario personalizado.
# Django lo necesita para saber cómo crear usuarios y superusuarios.
class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre, apellido, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es un campo obligatorio.')
        email = self.normalize_email(email)
        user = self.model(email=email, nombre=nombre, apellido=apellido, **extra_fields)
        user.set_password(password) # set_password se encarga de hacer el hash seguro
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, apellido, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, nombre, apellido, password, **extra_fields)

# Nuestro Modelo de Usuario Personalizado.
# Hereda de AbstractBaseUser para tener control total del modelo
# y de PermissionsMixin para integrar los permisos de Django.
class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=150, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    
    # Relación con el modelo Rol
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True) # Campo 'activo' de tu script
    is_staff = models.BooleanField(default=False) # Necesario para el admin de Django

    fecha_creacion = models.DateTimeField(default=timezone.now)

    objects = UsuarioManager()

    # Le decimos a Django que el campo 'email' será el usado para el login.
    USERNAME_FIELD = 'email'
    # Campos requeridos al crear un superusuario por consola.
    REQUIRED_FIELDS = ['nombre', 'apellido']

    def __str__(self):
        return self.email

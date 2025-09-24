
from django.db import models
from django.conf import settings # Para referenciar al modelo de Usuario

# Modelo Empresa
# Almacena la información principal de la compañía del cliente.
class Empresa(models.Model):
    # Usamos OneToOneField porque un usuario solo puede gestionar una empresa.
    # Si el usuario se elimina, la empresa asociada también se eliminará (CASCADE).
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nit = models.CharField(max_length=20, unique=True)
    razon_social = models.CharField(max_length=255)
    pais = models.CharField(max_length=100, blank=True)
    departamento = models.CharField(max_length=100, blank=True)
    municipio = models.CharField(max_length=100, blank=True)
    correo_principal = models.EmailField(max_length=150, blank=True)
    telefono_fijo = models.CharField(max_length=30, blank=True)
    telefono_movil = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.razon_social

# Modelo Sede
# Una empresa puede tener múltiples sedes.
class Sede(models.Model):
    # Relación ForeignKey: muchas sedes pueden pertenecer a una empresa.
    empresa = models.ForeignKey(Empresa, related_name='sedes', on_delete=models.CASCADE)
    direccion = models.TextField()
    pais = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)

    def __str__(self):
        return f"Sede de {self.empresa.razon_social} en {self.municipio}"

# Modelo RepresentanteLegal
# Cada empresa tiene un único representante legal.
class RepresentanteLegal(models.Model):
    # OneToOneField asegura que una empresa solo tenga un representante.
    empresa = models.OneToOneField(Empresa, on_delete=models.CASCADE)
    tipo_documento = models.CharField(max_length=30)
    numero_documento = models.CharField(max_length=30)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo_personal = models.EmailField(max_length=150)
    telefono_movil = models.CharField(max_length=30)

    # NOTA IMPORTANTE sobre los archivos (BYTEA vs FileField):
    # En Django, la mejor práctica no es guardar archivos en la base de datos (BYTEA)
    # porque es ineficiente. En su lugar, se usa un FileField que guarda el archivo
    # en el servidor y solo almacena la ruta en la base de datos.
    # Para usar FileField, necesitarás configurar MEDIA_ROOT y MEDIA_URL en settings.py
    documento_pdf = models.FileField(upload_to='representantes/documentos/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

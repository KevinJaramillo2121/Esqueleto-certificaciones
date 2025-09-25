# expedientes/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone

# Modelo Empresa
class Empresa(models.Model):
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
class Sede(models.Model):
    empresa = models.ForeignKey(Empresa, related_name='sedes', on_delete=models.CASCADE)
    direccion = models.TextField()
    pais = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)

    def __str__(self):
        return f"Sede de {self.empresa.razon_social} en {self.municipio}"

# Modelo RepresentanteLegal
class RepresentanteLegal(models.Model):
    empresa = models.OneToOneField(Empresa, on_delete=models.CASCADE)
    tipo_documento = models.CharField(max_length=30)
    numero_documento = models.CharField(max_length=30)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo_personal = models.EmailField(max_length=150)
    telefono_movil = models.CharField(max_length=30)
    documento_pdf = models.FileField(upload_to='representantes/documentos/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

# Modelo Solicitud
class Solicitud(models.Model):
    ESTADO_CHOICES = [
        ('Borrador', 'Borrador'),
        ('En Revisión', 'En Revisión'),
        ('En Subsanación', 'En Subsanación'),
        ('En Planificación', 'En Planificación'),
        ('En Ejecución', 'En Ejecución'),
        ('Revisión de Evidencias', 'Revisión de Evidencias'),
        ('Aprobado', 'Aprobado'),
        ('Rechazado', 'Rechazado'),
    ]
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='solicitudes')
    usuario_solicitante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='Borrador')
    observaciones = models.TextField(blank=True, null=True)
    esquema_certificacion = models.CharField(max_length=100, blank=True)
    sistema_gestion = models.TextField(blank=True, null=True, help_text="Aplicable para certificaciones bajo el esquema 6 de la norma ISO/IEC 17067:2013")

    def __str__(self):
        return f"SOL-{self.id:04d} - {self.empresa.razon_social}"

# Modelo Alcance
class Alcance(models.Model):
    TIPO_ALCANCE_CHOICES = [
        ('Producto', 'Producto'),
        ('Proceso', 'Proceso'),
        ('Servicio', 'Servicio'),
    ]
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='alcances')
    tipo = models.CharField(max_length=30, choices=TIPO_ALCANCE_CHOICES)
    descripcion = models.TextField()
    referencia_normativa = models.TextField(blank=True)
    esquema_certificacion = models.CharField(max_length=100, blank=True)
    revision_conforme = models.BooleanField(null=True, default=None, blank=True)
    revision_observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Alcance {self.tipo}: {self.descripcion[:50]}..."

# --- MODELOS DE RECURSOS (AHORA AL NIVEL CORRECTO) ---

class PersonaClave(models.Model):
    alcance = models.ForeignKey(Alcance, on_delete=models.CASCADE, related_name='personas_clave')
    nombres = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    formacion = models.CharField(max_length=100, blank=True)
    experiencia = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombres} - {self.cargo}"

class EquipoClave(models.Model):
    alcance = models.ForeignKey(Alcance, on_delete=models.CASCADE, related_name='equipos_clave')
    descripcion = models.TextField()
    identificacion_interna = models.CharField(max_length=50, blank=True)
    hoja_vida = models.FileField(upload_to='equipos/hojas_vida/', blank=True, null=True)

    def __str__(self):
        return self.descripcion

class DocumentoProceso(models.Model):
    alcance = models.ForeignKey(Alcance, on_delete=models.CASCADE, related_name='documentos_proceso')
    descripcion = models.TextField()
    nombre_archivo = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='documentos_proceso/')

    def __str__(self):
        return self.nombre_archivo


class Evaluador(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=30, blank=True)
    correo = models.EmailField(unique=True)
    # Según el documento de requisitos, para gestionar el costo por día.
    costo_dia = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # "Campo de acción" se puede interpretar como sus especialidades.
    campo_accion = models.TextField(blank=True, help_text="Describa las áreas de especialización, separadas por comas.")

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

# Nota: Más adelante añadiremos aquí los modelos, Revision, Certificado, etc.


class Actividad(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='actividades')
    evaluador_asignado = models.ForeignKey(Evaluador, on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=255, help_text="Ej: Auditoría en sitio, Revisión documental inicial")
    fecha_inicio_planificada = models.DateField()
    dias_planificados = models.PositiveIntegerField(default=1)
    fecha_limite_evidencias = models.DateField()
    
    # Este campo nos servirá más adelante en la Fase 6
    estado = models.CharField(max_length=50, default='Planificada')

    def __str__(self):
        return f"Actividad '{self.nombre}' para Solicitud {self.solicitud.id}"
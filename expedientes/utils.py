# expedientes/utils.py
from django.contrib.contenttypes.models import ContentType
from .models import Auditoria

def registrar_auditoria(usuario, objeto, accion_descripcion):
    """
    Crea una entrada en el log de auditoría asociada a un objeto específico.
    """
    Auditoria.objects.create(
        usuario=usuario,
        accion=accion_descripcion,
        content_type=ContentType.objects.get_for_model(objeto),
        object_id=objeto.pk
    )

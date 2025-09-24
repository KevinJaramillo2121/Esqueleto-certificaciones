# expedientes/urls.py
from django.urls import path
from .views import (
    DashboardView,
    EmpresaCreateView, EmpresaUpdateView,
    SedeCreateView, SedeUpdateView, SedeDeleteView,
    RepresentanteLegalCreateView, RepresentanteLegalUpdateView,
    SolicitudCreateView, SolicitudDetailView, EnviarSolicitudView,
    AlcanceCreateView, AlcanceUpdateView, AlcanceDeleteView, AlcanceDetailView,
    PersonaClaveCreateView, PersonaClaveUpdateView, PersonaClaveDeleteView,
    EquipoClaveCreateView, EquipoClaveUpdateView, EquipoClaveDeleteView,
    DocumentoProcesoCreateView, DocumentoProcesoUpdateView, DocumentoProcesoDeleteView,
)

urlpatterns = [
    # Dashboard Principal del Cliente
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
    # URLs de Empresa
    path('empresa/crear/', EmpresaCreateView.as_view(), name='empresa_crear'),
    path('empresa/editar/', EmpresaUpdateView.as_view(), name='empresa_editar'),
    
    # URLs para Sedes
    path('sede/crear/', SedeCreateView.as_view(), name='sede_crear'),
    path('sede/<int:pk>/editar/', SedeUpdateView.as_view(), name='sede_editar'),
    path('sede/<int:pk>/eliminar/', SedeDeleteView.as_view(), name='sede_eliminar'),

    # URLs para Representante Legal
    path('representante/crear/', RepresentanteLegalCreateView.as_view(), name='representante_crear'),
    path('representante/editar/', RepresentanteLegalUpdateView.as_view(), name='representante_editar'),

    # URLs para Solicitud
    path('solicitud/crear/', SolicitudCreateView.as_view(), name='solicitud_crear'),
    path('solicitud/<int:pk>/', SolicitudDetailView.as_view(), name='solicitud_detalle'),
    path('solicitud/<int:pk>/enviar/', EnviarSolicitudView.as_view(), name='solicitud_enviar'),

    # URLs para Alcance (anidadas bajo una solicitud)
    path('solicitud/<int:solicitud_pk>/alcance/crear/', AlcanceCreateView.as_view(), name='alcance_crear'),
    path('alcance/<int:pk>/editar/', AlcanceUpdateView.as_view(), name='alcance_editar'),
    path('alcance/<int:pk>/eliminar/', AlcanceDeleteView.as_view(), name='alcance_eliminar'),
    path('alcance/<int:pk>/', AlcanceDetailView.as_view(), name='alcance_detalle'),

    # URLs para PersonaClave (anidadas bajo un alcance)
    path('alcance/<int:alcance_pk>/persona/crear/', PersonaClaveCreateView.as_view(), name='persona_crear'),
    path('persona/<int:pk>/editar/', PersonaClaveUpdateView.as_view(), name='persona_editar'),
    path('persona/<int:pk>/eliminar/', PersonaClaveDeleteView.as_view(), name='persona_eliminar'),

    # URLs para EquipoClave
    path('alcance/<int:alcance_pk>/equipo/crear/', EquipoClaveCreateView.as_view(), name='equipo_crear'),
    path('equipo/<int:pk>/editar/', EquipoClaveUpdateView.as_view(), name='equipo_editar'),
    path('equipo/<int:pk>/eliminar/', EquipoClaveDeleteView.as_view(), name='equipo_eliminar'),

    # URLs para DocumentoProceso
    path('alcance/<int:alcance_pk>/documento/crear/', DocumentoProcesoCreateView.as_view(), name='documento_crear'),
    path('documento/<int:pk>/editar/', DocumentoProcesoUpdateView.as_view(), name='documento_editar'),
    path('documento/<int:pk>/eliminar/', DocumentoProcesoDeleteView.as_view(), name='documento_eliminar'),
]

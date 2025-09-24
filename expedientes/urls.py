# expedientes/urls.py
from django.urls import path
from .views import DashboardView, AlcanceCreateView, AlcanceUpdateView, AlcanceDeleteView, AlcanceDetailView, PersonaClaveCreateView, PersonaClaveUpdateView, PersonaClaveDeleteView, EquipoClaveCreateView, DocumentoProcesoCreateView
from .views import EmpresaCreateView, EnviarSolicitudView
from .views import EmpresaUpdateView, SedeCreateView, SedeDeleteView, SedeUpdateView, RepresentanteLegalCreateView, RepresentanteLegalUpdateView, SolicitudCreateView, SolicitudDetailView

urlpatterns = [
        # Dashboard del usuario
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

        # Aquí añadiremos las URLs para crear/editar empresa más adelante
    path('empresa/crear/', EmpresaCreateView.as_view(), name='empresa_crear'),

        # Nueva URL para editar la empresa
    path('empresa/editar/', EmpresaUpdateView.as_view(), name='empresa_editar'), 



            # URLs para gestionar sedes
        # Crear una nueva sede
    path('sede/crear/', SedeCreateView.as_view(), name='sede_crear'),   

        # Editar una sede existente
    path('sede/<int:pk>/editar/', SedeUpdateView.as_view(), name='sede_editar'),

        # Eliminar una sede existente
    path('sede/<int:pk>/eliminar/', SedeDeleteView.as_view(), name='sede_eliminar'),

        # URLs para gestionar el representante legal
    path('representante/crear/', RepresentanteLegalCreateView.as_view(), name='representante_crear'),

    # Editar un representante legal existente
    path('representante/editar/', RepresentanteLegalUpdateView.as_view(), name='representante_editar'),

    # Aquí añadiremos las URLs para crear/editar solicitudes más adelante
    path('solicitud/crear/', SolicitudCreateView.as_view(), name='solicitud_crear'),
    # La <int:pk> captura el número de ID de la solicitud desde la URL
    # y se lo pasa a la DetailView.
    path('solicitud/<int:pk>/', SolicitudDetailView.as_view(), name='solicitud_detalle'),

    # URLs para Alcance (anidadas bajo una solicitud)
    path('solicitud/<int:solicitud_pk>/alcance/crear/', AlcanceCreateView.as_view(), name='alcance_crear'),

    path('alcance/<int:pk>/editar/', AlcanceUpdateView.as_view(), name='alcance_editar'),
    
    path('alcance/<int:pk>/eliminar/', AlcanceDeleteView.as_view(), name='alcance_eliminar'),

    path('alcance/<int:pk>/', AlcanceDetailView.as_view(), name='alcance_detalle'),

    # URLs para PersonaClave (anidadas bajo un alcance)
    path('alcance/<int:alcance_pk>/persona/crear/', PersonaClaveCreateView.as_view(), name='persona_crear'),
    path('persona/<int:pk>/editar/', PersonaClaveUpdateView.as_view(), name='persona_editar'),
    path('persona/<int:pk>/eliminar/', PersonaClaveDeleteView.as_view(), name='persona_eliminar'),

    # Nuevas URLs para recursos
    path('alcance/<int:alcance_pk>/equipo/crear/', EquipoClaveCreateView.as_view(), name='equipo_crear'),
    path('alcance/<int:alcance_pk>/documento/crear/', DocumentoProcesoCreateView.as_view(), name='documento_crear'),

    # URL para enviar la solicitud (cambiar estado a "En Revisión")
    path('solicitud/<int:pk>/enviar/', EnviarSolicitudView.as_view(), name='solicitud_enviar'),


]



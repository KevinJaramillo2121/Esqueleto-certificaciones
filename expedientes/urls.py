# expedientes/urls.py
from django.urls import path
from .views import DashboardView
from .views import EmpresaCreateView
from .views import EmpresaUpdateView, SedeCreateView, SedeDeleteView, SedeUpdateView, RepresentanteLegalCreateView, RepresentanteLegalUpdateView

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

]

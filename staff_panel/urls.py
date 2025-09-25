# staff_panel/urls.py
from django.urls import path
from .views import (
    StaffDashboardView, SolicitudRevisionView,
    EvaluadorListView, EvaluadorCreateView, EvaluadorUpdateView, EvaluadorDeleteView, SolicitudPlanificacionView, IniciarEjecucionView
)

urlpatterns = [
    path('staff/dashboard/', StaffDashboardView.as_view(), name='staff_dashboard'),
    
    path('staff/solicitud/<int:pk>/revision/', SolicitudRevisionView.as_view(), name='solicitud_revision'),

    path('staff/evaluadores/', EvaluadorListView.as_view(), name='evaluador_list'),
    path('staff/evaluadores/crear/', EvaluadorCreateView.as_view(), name='evaluador_crear'),
    path('staff/evaluadores/<int:pk>/editar/', EvaluadorUpdateView.as_view(), name='evaluador_editar'),
    path('staff/evaluadores/<int:pk>/eliminar/', EvaluadorDeleteView.as_view(), name='evaluador_eliminar'),

        # Nueva ruta para la planificación de la solicitud
    path('staff/solicitud/<int:pk>/planificar/', SolicitudPlanificacionView.as_view(), name='solicitud_planificar'),

        # Nueva ruta para iniciar la ejecución de la solicitud
    path('staff/solicitud/<int:pk>/iniciar_ejecucion/', IniciarEjecucionView.as_view(), name='iniciar_ejecucion'),

]

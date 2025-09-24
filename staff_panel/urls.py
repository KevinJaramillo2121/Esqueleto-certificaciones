# staff_panel/urls.py
from django.urls import path
from .views import StaffDashboardView, SolicitudRevisionView

urlpatterns = [
    path('staff/dashboard/', StaffDashboardView.as_view(), name='staff_dashboard'),
    
    path('staff/solicitud/<int:pk>/revision/', SolicitudRevisionView.as_view(), name='solicitud_revision'),
]

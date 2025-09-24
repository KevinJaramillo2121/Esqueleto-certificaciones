# expedientes/urls.py
from django.urls import path
from .views import DashboardView
from .views import EmpresaCreateView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # Aquí añadiremos las URLs para crear/editar empresa más adelante
    path('empresa/crear/', EmpresaCreateView.as_view(), name='empresa_crear'),

]

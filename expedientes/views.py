# expedientes/views.py
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Empresa
from .forms import EmpresaForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

# Usamos LoginRequiredMixin para proteger esta vista.
# Si un usuario no autenticado intenta acceder, será redirigido al login.
class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Buscamos si el usuario ya tiene una empresa creada.
        try:
            empresa = request.user.empresa
        except Empresa.DoesNotExist:
            empresa = None
        
        context = {
            'empresa': empresa
        }
        return render(request, 'expedientes/dashboard.html', context)

# Create your views here.
class EmpresaCreateView(LoginRequiredMixin, CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'expedientes/empresa_form.html'
    success_url = reverse_lazy('dashboard') # Redirige al dashboard tras el éxito

    # Este método es crucial: asigna automáticamente el usuario logueado
    # al campo 'usuario' de la nueva empresa antes de guardarla.
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)
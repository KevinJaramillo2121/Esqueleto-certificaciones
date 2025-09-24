# expedientes/views.py
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Empresa, Sede, RepresentanteLegal
from .forms import EmpresaForm, SedeForm, RepresentanteLegalForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView


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
    
# Vista para editar la empresa del usuario
    # Apartir de esta vista, el usuario podrá editar la información de su empresa.
    
class EmpresaUpdateView(LoginRequiredMixin, UpdateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'expedientes/empresa_form.html' # Reutilizamos el mismo formulario
    success_url = reverse_lazy('dashboard')

    # Este método asegura que el usuario solo pueda editar SU propia empresa
    def get_object(self, queryset=None):
        return self.request.user.empresa
    
    # Mixin para filtrar objetos por la empresa del usuario
class OwnObjectsMixin:
    def get_queryset(self):
        return self.model.objects.filter(empresa=self.request.user.empresa)
    
    # Vista para crear una nueva sede asociada a la empresa del usuario
class SedeCreateView(LoginRequiredMixin, CreateView):
    model = Sede
    form_class = SedeForm
    template_name = 'expedientes/sede_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)

    # Vista para editar una sede existente
class SedeUpdateView(LoginRequiredMixin, OwnObjectsMixin, UpdateView):
    model = Sede
    form_class = SedeForm
    template_name = 'expedientes/sede_form.html'
    success_url = reverse_lazy('dashboard')

    # El queryset ya está filtrado por OwnObjectsMixin
class SedeDeleteView(LoginRequiredMixin, OwnObjectsMixin, DeleteView):
    model = Sede
    template_name = 'expedientes/sede_confirm_delete.html'
    success_url = reverse_lazy('dashboard')


    # Vista para crear o editar el representante legal de la empresa
class RepresentanteLegalCreateView(LoginRequiredMixin, CreateView):
    model = RepresentanteLegal
    form_class = RepresentanteLegalForm
    template_name = 'expedientes/representante_form.html'
    success_url = reverse_lazy('dashboard')

    # Al guardar, asignamos el representante a la empresa del usuario actual.
    def form_valid(self, form):
        form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)

class RepresentanteLegalUpdateView(LoginRequiredMixin, UpdateView):
    model = RepresentanteLegal
    form_class = RepresentanteLegalForm
    template_name = 'expedientes/representante_form.html'
    success_url = reverse_lazy('dashboard')

    # Este método es clave: asegura que el usuario solo pueda editar
    # el representante legal asociado a SU empresa.
    def get_object(self, queryset=None):
        return self.request.user.empresa.representantelegal

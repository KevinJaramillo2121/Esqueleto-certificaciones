# expedientes/views.py
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Empresa, Sede, RepresentanteLegal, Solicitud
from .forms import EmpresaForm, SedeForm, RepresentanteLegalForm, SolicitudForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib import messages 


# Usamos LoginRequiredMixin para proteger esta vista.
# Si un usuario no autenticado intenta acceder, será redirigido al login.
class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        empresa = None
        solicitudes = None # Inicializamos la variable
        try:
            empresa = request.user.empresa
            # Si la empresa existe, obtenemos sus solicitudes
            solicitudes = empresa.solicitudes.all().order_by('-fecha_creacion')
        except Empresa.DoesNotExist:
            pass # No hace nada si la empresa no existe
        
        context = {
            'empresa': empresa,
            'solicitudes': solicitudes, # Pasamos las solicitudes a la plantilla
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

class SolicitudCreateView(LoginRequiredMixin, CreateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = 'expedientes/solicitud_form.html'
    
    # Redirigiremos a la página de detalle de la solicitud recién creada (la haremos después)
    def get_success_url(self):
        return reverse_lazy('solicitud_detalle', kwargs={'pk': self.object.pk})

    # Este método se ejecuta ANTES que cualquier otro.
    # Es el lugar perfecto para verificar si el usuario cumple los requisitos.
    def dispatch(self, request, *args, **kwargs):
        try:
            # Comprueba si la empresa y el representante legal existen.
            empresa = request.user.empresa
            representante = empresa.representantelegal
        except (Empresa.DoesNotExist, RepresentanteLegal.DoesNotExist):
            # Si algo falta, muestra un mensaje de error y redirige al dashboard.
            messages.error(request, 'Debe completar la información de la Empresa y del Representante Legal antes de crear una solicitud.')
            return redirect('dashboard')
        
        return super().dispatch(request, *args, **kwargs)

    # Cuando el formulario es válido, asignamos los datos automáticos.
    def form_valid(self, form):
        form.instance.empresa = self.request.user.empresa
        form.instance.usuario_solicitante = self.request.user
        messages.success(self.request, '¡Solicitud iniciada con éxito! Ahora puede añadir el alcance de la certificación.')
        return super().form_valid(form)
# expedientes/views.py
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from users.mixins import StaffRequiredMixin
from .models import Auditoria, Empresa, Sede, RepresentanteLegal, Solicitud, Alcance, PersonaClave, EquipoClave, DocumentoProceso
from .forms import EmpresaForm, SedeForm, RepresentanteLegalForm, SolicitudForm, AlcanceForm, PersonaClaveForm, EquipoClaveForm, DocumentoProcesoForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib import messages 
from django.shortcuts import get_object_or_404 # <-- Importa esta función
from .utils import registrar_auditoria 
from django.contrib.contenttypes.models import ContentType

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
    

class SolicitudDetailView(LoginRequiredMixin, DetailView):
    model = Solicitud
    template_name = 'expedientes/solicitud_detalle.html'
    context_object_name = 'solicitud' # Nombre que usaremos en la plantilla

    # ¡Paso de seguridad CRUCIAL!
    # Este método asegura que un usuario solo pueda ver las solicitudes
    # que pertenecen a su propia empresa. Si alguien intenta acceder a una
    # solicitud de otra empresa por la URL, recibirá un error 404 (No Encontrado).
    def get_queryset(self):
        return Solicitud.objects.filter(empresa=self.request.user.empresa)

class AlcanceCreateView(LoginRequiredMixin, CreateView):
    # ... (código existente)
    def dispatch(self, request, *args, **kwargs):
        self.solicitud = get_object_or_404(Solicitud, pk=self.kwargs['solicitud_pk'], empresa=request.user.empresa)
        # Modificamos la condición
        if self.solicitud.estado not in ['Borrador', 'En Subsanación']:
            messages.error(request, 'No se puede modificar una solicitud que no está en estado Borrador o En Subsanación.')
            return redirect('solicitud_detalle', pk=self.solicitud.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Asignar la solicitud al nuevo alcance
        form.instance.solicitud = self.solicitud
        messages.success(self.request, 'Ítem de alcance añadido con éxito.')
        return super().form_valid(form)

    def get_success_url(self):
        # Redirigir de vuelta a la página de detalle de la solicitud
        return reverse_lazy('solicitud_detalle', kwargs={'pk': self.solicitud.pk})

class AlcanceUpdateView(LoginRequiredMixin, UpdateView):
    model = Alcance
    form_class = AlcanceForm
    template_name = 'expedientes/alcance_form.html'

    def get_queryset(self):
        # Asegurar que el usuario solo puede editar alcances de sus propias solicitudes
        return Alcance.objects.filter(solicitud__empresa=self.request.user.empresa)

    def get_success_url(self):
        messages.success(self.request, 'Ítem de alcance actualizado con éxito.')
        return reverse_lazy('solicitud_detalle', kwargs={'pk': self.object.solicitud.pk})

class AlcanceDeleteView(LoginRequiredMixin, DeleteView):
    model = Alcance
    template_name = 'expedientes/alcance_confirm_delete.html'
    context_object_name = 'alcance'

    def get_queryset(self):
        return Alcance.objects.filter(solicitud__empresa=self.request.user.empresa)

    def get_success_url(self):
        messages.success(self.request, 'Ítem de alcance eliminado con éxito.')
        return reverse_lazy('solicitud_detalle', kwargs={'pk': self.object.solicitud.pk})
    
class AlcanceDetailView(LoginRequiredMixin, DetailView):
    model = Alcance
    template_name = 'expedientes/alcance_detalle.html'
    context_object_name = 'alcance'

    def get_queryset(self):
        # Seguridad: solo se pueden ver alcances de las solicitudes del usuario.
        return Alcance.objects.filter(solicitud__empresa=self.request.user.empresa)
    
class PersonaClaveCreateView(LoginRequiredMixin, CreateView):
    from .models import PersonaClave
    from .forms import PersonaClaveForm
    
    model = PersonaClave
    form_class = PersonaClaveForm
    template_name = 'expedientes/generic_form.html'

    def dispatch(self, request, *args, **kwargs):
        from .models import Alcance
        self.alcance = get_object_or_404(Alcance, pk=self.kwargs['alcance_pk'], solicitud__empresa=request.user.empresa)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.alcance = self.alcance
        messages.success(self.request, 'Persona clave añadida con éxito.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('alcance_detalle', kwargs={'pk': self.alcance.pk})

class PersonaClaveUpdateView(LoginRequiredMixin, UpdateView):
    from .models import PersonaClave
    from .forms import PersonaClaveForm

    model = PersonaClave
    form_class = PersonaClaveForm
    template_name = 'expedientes/generic_form.html'

    def get_queryset(self):
        return self.model.objects.filter(alcance__solicitud__empresa=self.request.user.empresa)
    
    def get_success_url(self):
        messages.success(self.request, 'Persona clave actualizada con éxito.')
        return reverse_lazy('alcance_detalle', kwargs={'pk': self.object.alcance.pk})


class PersonaClaveDeleteView(LoginRequiredMixin, DeleteView):
    from .models import PersonaClave
    
    model = PersonaClave
    template_name = 'expedientes/generic_confirm_delete.html'
    context_object_name = 'object'

    def get_queryset(self):
        return self.model.objects.filter(alcance__solicitud__empresa=self.request.user.empresa)

    def get_success_url(self):
        messages.success(self.request, 'Persona clave eliminada con éxito.')
        return reverse_lazy('alcance_detalle', kwargs={'pk': self.object.alcance.pk})

# --- Vistas para EquipoClave ---
class EquipoClaveCreateView(LoginRequiredMixin, CreateView):
    from .models import EquipoClave
    from .forms import EquipoClaveForm

    model = EquipoClave
    form_class = EquipoClaveForm
    template_name = 'expedientes/generic_form.html'

    def dispatch(self, request, *args, **kwargs):
        from .models import Alcance
        self.alcance = get_object_or_404(Alcance, pk=self.kwargs['alcance_pk'], solicitud__empresa=request.user.empresa)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.alcance = self.alcance
        messages.success(self.request, 'Equipo clave añadido con éxito.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('alcance_detalle', kwargs={'pk': self.alcance.pk})

class EquipoClaveUpdateView(LoginRequiredMixin, UpdateView):
    from .models import EquipoClave
    from .forms import EquipoClaveForm

    model = EquipoClave
    form_class = EquipoClaveForm
    template_name = 'expedientes/generic_form.html'

    def get_queryset(self):
        return self.model.objects.filter(alcance__solicitud__empresa=self.request.user.empresa)
    
    def get_success_url(self):
        messages.success(self.request, 'Equipo clave actualizado con éxito.')
        return reverse_lazy('alcance_detalle', kwargs={'pk': self.object.alcance.pk})

class EquipoClaveDeleteView(LoginRequiredMixin, DeleteView):
    from .models import EquipoClave
    
    model = EquipoClave
    template_name = 'expedientes/generic_confirm_delete.html'
    context_object_name = 'object'

    def get_queryset(self):
        return self.model.objects.filter(alcance__solicitud__empresa=self.request.user.empresa)

    def get_success_url(self):
        messages.success(self.request, 'Equipo clave eliminado con éxito.')
        return reverse_lazy('alcance_detalle', kwargs={'pk': self.object.alcance.pk})


# --- Vistas para DocumentoProceso ---
class DocumentoProcesoCreateView(LoginRequiredMixin, CreateView):
    from .models import DocumentoProceso
    from .forms import DocumentoProcesoForm

    model = DocumentoProceso
    form_class = DocumentoProcesoForm
    template_name = 'expedientes/generic_form.html'

    def dispatch(self, request, *args, **kwargs):
        from .models import Alcance
        self.alcance = get_object_or_404(Alcance, pk=self.kwargs['alcance_pk'], solicitud__empresa=request.user.empresa)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.alcance = self.alcance
        messages.success(self.request, 'Documento añadido con éxito.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('alcance_detalle', kwargs={'pk': self.alcance.pk})

class DocumentoProcesoUpdateView(LoginRequiredMixin, UpdateView):
    from .models import DocumentoProceso
    from .forms import DocumentoProcesoForm

    model = DocumentoProceso
    form_class = DocumentoProcesoForm
    template_name = 'expedientes/generic_form.html'

    def get_queryset(self):
        return self.model.objects.filter(alcance__solicitud__empresa=self.request.user.empresa)
    
    def get_success_url(self):
        messages.success(self.request, 'Documento actualizado con éxito.')
        return reverse_lazy('alcance_detalle', kwargs={'pk': self.object.alcance.pk})

class DocumentoProcesoDeleteView(LoginRequiredMixin, DeleteView):
    from .models import DocumentoProceso
    
    model = DocumentoProceso
    template_name = 'expedientes/generic_confirm_delete.html'
    context_object_name = 'object'

    def get_queryset(self):
        return self.model.objects.filter(alcance__solicitud__empresa=self.request.user.empresa)

    def get_success_url(self):
        messages.success(self.request, 'Documento eliminado con éxito.')
        return reverse_lazy('alcance_detalle', kwargs={'pk': self.object.alcance.pk})
    

class EnviarSolicitudView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        solicitud = get_object_or_404(Solicitud, pk=self.kwargs['pk'], empresa=request.user.empresa)

        # Modificamos la validación de estado
        if solicitud.estado not in ['Borrador', 'En Subsanación']:
            messages.error(request, 'Esta solicitud no se puede enviar.')
            return redirect('solicitud_detalle', pk=solicitud.pk)

        if not solicitud.alcances.exists():
            messages.error(request, 'No puede enviar una solicitud sin al menos un ítem al alcance.')
            return redirect('solicitud_detalle', pk=solicitud.pk)

        # ¡Paso clave! Limpiamos las revisiones anteriores antes de reenviar.
        # Esto resetea el estado de revisión para que el personal pueda empezar de cero.
        for alcance in solicitud.alcances.all():
            alcance.revision_conforme = None
            alcance.revision_observaciones = ""
            alcance.save()

        # Cambiamos el estado y guardamos
        solicitud.estado = 'En Revisión'
        solicitud.save()

        registrar_auditoria(request.user, solicitud, "Solicitud enviada a revisión.")


        messages.success(request, '¡Solicitud enviada a revisión con éxito!')
        return redirect('solicitud_detalle', pk=solicitud.pk)

class ExpedienteHistorialView(StaffRequiredMixin, DetailView):
    
    model = Solicitud
    template_name = 'staff_panel/expediente_historial.html'
    context_object_name = 'solicitud'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        solicitud_type = ContentType.objects.get_for_model(self.object)
        context['historial'] = Auditoria.objects.filter(
            content_type=solicitud_type,
            object_id=self.object.pk
        )
        return context
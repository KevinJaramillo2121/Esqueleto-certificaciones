# staff_panel/views.py
from django.shortcuts import render
from django.views import View
from users.mixins import StaffRequiredMixin # <-- Importamos nuestro mixin
from expedientes.models import Solicitud
from .forms import AlcanceRevisionFormSet, EvaluadorForm # <-- Importamos nuestro FormSet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from expedientes.models import Evaluador 
from .forms import ActividadFormSet # <-- Importa el nuevo FormSet


        # Vista del panel de staff
class StaffDashboardView(StaffRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        solicitudes_por_revisar = Solicitud.objects.filter(estado='En Revisión').order_by('fecha_creacion')
        # NUEVA QUERY
        solicitudes_por_planificar = Solicitud.objects.filter(estado='En Planificación').order_by('fecha_creacion')

        context = {
            'solicitudes_por_revisar': solicitudes_por_revisar,
            'solicitudes_por_planificar': solicitudes_por_planificar, # NUEVO CONTEXTO
        }
        return render(request, 'staff_panel/staff_dashboard.html', context)


        # Vista para revisar una solicitud específica
class SolicitudRevisionView(StaffRequiredMixin, View):
    template_name = 'staff_panel/solicitud_revision_form.html'

    def get(self, request, *args, **kwargs):
        solicitud = get_object_or_404(Solicitud, pk=kwargs['pk'])
        formset = AlcanceRevisionFormSet(instance=solicitud)
        
        context = {
            'solicitud': solicitud,
            'formset': formset
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        solicitud = get_object_or_404(Solicitud, pk=kwargs['pk'])
        formset = AlcanceRevisionFormSet(request.POST, instance=solicitud)

        if formset.is_valid():
            formset.save()

            # Lógica para decidir el siguiente estado
            todos_conformes = all(alcance.revision_conforme for alcance in solicitud.alcances.all() if alcance.revision_conforme is not None)
            hay_no_conformes = any(alcance.revision_conforme is False for alcance in solicitud.alcances.all())

            if hay_no_conformes:
                solicitud.estado = 'En Subsanación'
                messages.warning(request, 'La solicitud ha sido devuelta al cliente con observaciones.')
            elif todos_conformes:
                solicitud.estado = 'En Planificación'
                messages.success(request, 'La solicitud ha sido aprobada y ha pasado a planificación.')
            
            solicitud.save()
            return redirect('staff_dashboard')
        
        context = {
            'solicitud': solicitud,
            'formset': formset
        }
        messages.error(request, 'Hubo un error al procesar el formulario. Por favor, revisa los datos.')
        return render(request, self.template_name, context)


        # Vistas para la gestión de Evaluadores
class EvaluadorListView(StaffRequiredMixin, ListView):
    model = Evaluador
    template_name = 'staff_panel/evaluador_list.html'
    context_object_name = 'evaluadores'


        # Vista para crear un nuevo evaluador
class EvaluadorCreateView(StaffRequiredMixin, CreateView):
    model = Evaluador
    form_class = EvaluadorForm
    template_name = 'staff_panel/evaluador_form.html'
    success_url = reverse_lazy('evaluador_list')


        # Vista para editar un evaluador
class EvaluadorUpdateView(StaffRequiredMixin, UpdateView):
    model = Evaluador
    form_class = EvaluadorForm
    template_name = 'staff_panel/evaluador_form.html'
    success_url = reverse_lazy('evaluador_list')


        # Vista para eliminar un evaluador
class EvaluadorDeleteView(StaffRequiredMixin, DeleteView):
    model = Evaluador
    template_name = 'staff_panel/evaluador_confirm_delete.html'
    success_url = reverse_lazy('evaluador_list')
    context_object_name = 'evaluador'

        # Nueva vista para la planificación de la solicitud
class SolicitudPlanificacionView(StaffRequiredMixin, View):
    template_name = 'staff_panel/solicitud_planificacion.html'

    def get(self, request, *args, **kwargs):
        solicitud = get_object_or_404(Solicitud, pk=kwargs['pk'], estado='En Planificación')
        formset = ActividadFormSet(instance=solicitud)
        return render(request, self.template_name, {'solicitud': solicitud, 'formset': formset})

    def post(self, request, *args, **kwargs):
        solicitud = get_object_or_404(Solicitud, pk=kwargs['pk'], estado='En Planificación')
        formset = ActividadFormSet(request.POST, instance=solicitud)

        if formset.is_valid():
            formset.save()
            messages.success(request, 'Plan de evaluación guardado correctamente.')
            return redirect('staff_dashboard')
        
        messages.error(request, 'Por favor, corrige los errores en el formulario.')
        return render(request, self.template_name, {'solicitud': solicitud, 'formset': formset})

        # Vista para iniciar la ejecución de la solicitud
class IniciarEjecucionView(StaffRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # Obtenemos la solicitud de forma segura
        solicitud = get_object_or_404(Solicitud, pk=kwargs['pk'], estado='En Planificación')

        # --- Validación de Negocio Crítica ---
        # No se puede iniciar la ejecución si no se ha planificado al menos una actividad.
        if not solicitud.actividades.exists():
            messages.error(request, 'No se puede iniciar la ejecución sin haber planificado al menos una actividad.')
            return redirect('solicitud_planificar', pk=solicitud.pk)

        # ¡Acción principal! Cambiamos el estado
        solicitud.estado = 'En Ejecución'
        solicitud.save()

        messages.success(request, f'La solicitud {solicitud} ha pasado al estado "En Ejecución". Las tareas ahora serán visibles para los evaluadores asignados.')
        return redirect('staff_dashboard')
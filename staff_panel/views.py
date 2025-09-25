# staff_panel/views.py
from django.shortcuts import render
from django.views import View
from users.mixins import StaffRequiredMixin, EvaluadorRequiredMixin, RevisorRequiredMixin # <-- Importamos nuestro mixin
from expedientes.models import Solicitud
from .forms import AlcanceRevisionFormSet, EvaluadorForm, EvidenciaForm, EvidenciaRevisionFormSet # <-- Importamos nuestro FormSet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from expedientes.models import Evaluador, Actividad, Evidencia
from .forms import ActividadFormSet # <-- Importa el nuevo FormSet


        # Vista del panel de staff
class StaffDashboardView(StaffRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # ... (queries existentes) ...
        solicitudes_por_planificar = Solicitud.objects.filter(estado='En Planificación')
        # NUEVA QUERY
        solicitudes_en_ejecucion = Solicitud.objects.filter(estado='En Ejecución')

        context = {
            # ... (contexto existente) ...
            'solicitudes_por_planificar': solicitudes_por_planificar,
            'solicitudes_en_ejecucion': solicitudes_en_ejecucion, # NUEVO
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

        solicitud.actividades.update(estado='En Ejecución')

        messages.success(request, f'La solicitud {solicitud} ha pasado al estado "En Ejecución". Las tareas ahora serán visibles para los evaluadores asignados.')
        return redirect('staff_dashboard')


        # Nueva vista para el dashboard del evaluador
class EvaluadorDashboardView(EvaluadorRequiredMixin, ListView):
    model = Actividad
    template_name = 'staff_panel/evaluador_dashboard.html'
    context_object_name = 'actividades_asignadas'

    def get_queryset(self):
        # Filtramos las actividades para mostrar solo las asignadas al evaluador logueado
        # y que pertenecen a una solicitud que está "En Ejecución".
        return Actividad.objects.filter(
            evaluador_asignado=self.request.user.perfil_evaluador,
            solicitud__estado='En Ejecución'
        ).order_by('fecha_inicio_planificada')


        # Vista para ver los detalles de una actividad y subir evidencias
class ActividadDetailView(EvaluadorRequiredMixin, View):
    template_name = 'staff_panel/actividad_detail.html'

    def get(self, request, *args, **kwargs):
        # Obtenemos la actividad, asegurando que pertenece al evaluador logueado
        actividad = get_object_or_404(
            Actividad, 
            pk=kwargs['pk'], 
            evaluador_asignado=request.user.perfil_evaluador
        )
        
        form = EvidenciaForm()
        evidencias = actividad.evidencias.all().order_by('-fecha_carga')

        context = {
            'actividad': actividad,
            'evidencias': evidencias,
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        actividad = get_object_or_404(
            Actividad, 
            pk=kwargs['pk'], 
            evaluador_asignado=request.user.perfil_evaluador
        )
        
        form = EvidenciaForm(request.POST, request.FILES)
        
        if form.is_valid():
            nueva_evidencia = form.save(commit=False)
            nueva_evidencia.actividad = actividad
            nueva_evidencia.save()
            messages.success(request, 'Evidencia subida correctamente.')

            # --- LÓGICA CONDICIONAL CORRECTA ---
            # Solo si la actividad fue devuelta, la marcamos como corregida.
            if actividad.estado == 'Con Inconsistencias':
                # Limpiamos las marcas de revisión de TODAS las evidencias de esta actividad
                actividad.evidencias.update(revision_conforme=None, revision_observaciones='')
                # Devolvemos la actividad a su estado de trabajo normal
                actividad.estado = 'En Ejecución'
                actividad.save()
                messages.info(request, 'La actividad ha sido marcada como corregida y enviada nuevamente a revisión.')
            
            return redirect('actividad_detail', pk=actividad.pk)

        # Si el formulario no es válido, se mantiene el flujo de error.
        evidencias = actividad.evidencias.all().order_by('-fecha_carga')
        context = {
            'actividad': actividad,
            'evidencias': evidencias,
            'form': form
        }
        messages.error(request, 'Hubo un error al subir el archivo. Por favor, inténtalo de nuevo.')
        return render(request, self.template_name, context)

class SolicitudEvidenciaRevisionView(RevisorRequiredMixin, View):
    template_name = 'staff_panel/solicitud_evidencia_revision.html'

    def get(self, request, *args, **kwargs):
        solicitud = get_object_or_404(Solicitud, pk=kwargs['pk'], estado='En Ejecución')
        # Obtenemos todas las evidencias relacionadas con esta solicitud
        queryset = Evidencia.objects.filter(actividad__solicitud=solicitud).order_by('actividad__nombre')
        formset = EvidenciaRevisionFormSet(queryset=queryset)
        
        context = {'solicitud': solicitud, 'formset': formset}
        return render(request, self.template_name, context)

def post(self, request, *args, **kwargs):
        solicitud = get_object_or_404(Solicitud, pk=kwargs['pk'], estado='En Ejecución')
        queryset = Evidencia.objects.filter(actividad__solicitud=solicitud)
        formset = EvidenciaRevisionFormSet(request.POST, queryset=queryset)

        if formset.is_valid():
            formset.save()

            # Actualizamos el estado de cada actividad individualmente
            for actividad in solicitud.actividades.all():
                evidencias_actividad = actividad.evidencias.all()
                if not evidencias_actividad:
                    continue # La actividad no tiene evidencias, la ignoramos

                # Si alguna evidencia de esta actividad fue rechazada
                if any(ev.revision_conforme is False for ev in evidencias_actividad):
                    actividad.estado = 'Con Inconsistencias'
                # Si todas las evidencias fueron revisadas y todas están conformes
                elif all(ev.revision_conforme is True for ev in evidencias_actividad):
                    actividad.estado = 'Completada'
                actividad.save()

            # Finalmente, comprobamos el estado general de la solicitud
            todas_actividades_completadas = all(
                act.estado == 'Completada' for act in solicitud.actividades.all()
            )
            if todas_actividades_completadas:
                solicitud.estado = 'Revisión de Evidencias' # Estado final de la fase
                solicitud.save()
                messages.success(request, 'Todas las evidencias han sido aprobadas. La solicitud pasa a Revisión Final.')
            else:
                messages.warning(request, 'Se han guardado las revisiones. Algunas actividades han sido devueltas a los evaluadores con observaciones.')

            return redirect('staff_dashboard')
        

        context = {'solicitud': solicitud, 'formset': formset}
        return render(request, self.template_name, context)
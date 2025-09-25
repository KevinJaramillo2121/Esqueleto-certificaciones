# staff_panel/views.py
from django.shortcuts import render
from django.views import View
from users.mixins import StaffRequiredMixin, EvaluadorRequiredMixin, RevisorRequiredMixin, DirectorRequiredMixin
from expedientes.models import Solicitud, Certificado, Incidencia
from .forms import AlcanceRevisionFormSet, EvaluadorForm, EvidenciaForm, EvidenciaRevisionFormSet, IncidenciaForm # <-- Importamos nuestro FormSet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from expedientes.models import Evaluador, Actividad, Evidencia
from .forms import ActividadFormSet # <-- Importa el nuevo FormSet
from django.views.generic import DetailView
from datetime import date, timedelta
from django.template.loader import get_template
from django.http import HttpResponse
from expedientes.utils import registrar_auditoria # <-- Importa la función
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from expedientes.models import Auditoria



        # Vista del panel de staff
class StaffDashboardView(StaffRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # ... (queries existentes) ...
        solicitudes_por_planificar = Solicitud.objects.filter(estado='En Planificación')
        # NUEVA QUERY
        solicitudes_en_ejecucion = Solicitud.objects.filter(estado='En Ejecución')

        # NUEVA QUERY
        solicitudes_para_decision = Solicitud.objects.filter(estado='Revisión de Evidencias')

        # Ejemplo: Obtener todas las solicitudes aprobadas
        solicitudes_aprobadas = Solicitud.objects.filter(estado='Aprobado')
        context['solicitudes_aprobadas'] = solicitudes_aprobadas

        context = {
            # ... (contexto existente) ...
            'solicitudes_por_planificar': solicitudes_por_planificar,
            'solicitudes_en_ejecucion': solicitudes_en_ejecucion, # NUEVO
            'solicitudes_para_decision': solicitudes_para_decision, 
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

            if solicitud.estado == 'En Planificación':
                registrar_auditoria(request.user, solicitud, "Revisión de solicitud completada. Todos los ítems conformes.")
            else:
                registrar_auditoria(request.user, solicitud, "Revisión de solicitud completada. Se encontraron no conformidades.")

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

        registrar_auditoria(request.user, solicitud, "Planificación confirmada. Se inició la fase de ejecución.")


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

class ExpedienteDecisionView(DirectorRequiredMixin, DetailView):
    model = Solicitud
    template_name = 'staff_panel/expediente_decision.html'
    context_object_name = 'solicitud'

    def get_queryset(self):
        # El Director puede ver cualquier solicitud en este estado.
        return Solicitud.objects.filter(estado='Revisión de Evidencias')
    

class ExpedienteAprobarView(DirectorRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        solicitud = get_object_or_404(Solicitud, pk=kwargs['pk'], estado='Revisión de Evidencias')
        
        # Cambiamos el estado final
        solicitud.estado = 'Aprobado'
        solicitud.save()
        
        registrar_auditoria(request.user, solicitud, "Expediente APROBADO. Decisión final tomada.")
        
        messages.success(request, f'El expediente {solicitud} ha sido APROBADO con éxito. Ya puede proceder a emitir el certificado.')
        return redirect('staff_dashboard')
    
class GenerarCertificadoPDFView(DirectorRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        from weasyprint import HTML

        solicitud = get_object_or_404(Solicitud, pk=kwargs['pk'], estado='Aprobado')
        
        # 1. Generar datos del certificado
        # Podrías crear una lógica más compleja para el código si quieres.
        codigo_certificado = f"AOX-CERT-{solicitud.id:04d}-{date.today().year}"
        fecha_emision = date.today()
        # Asumimos que los certificados duran 3 años.
        fecha_vencimiento = fecha_emision + timedelta(days=3*365)

        # 2. Preparar el contexto para la plantilla
        context = {
            'solicitud': solicitud,
            'codigo_certificado': codigo_certificado,
            'fecha_emision': fecha_emision,
            'fecha_vencimiento': fecha_vencimiento,
        }

        # 3. Renderizar la plantilla HTML
        template = get_template('staff_panel/certificado_template.html')
        html_string = template.render(context)

        # 4. Generar el PDF con WeasyPrint
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        pdf = html.write_pdf()

        # 5. Guardar registro en la base de datos (opcional pero recomendado)
        # Primero, borramos cualquier certificado antiguo para esta solicitud
        Certificado.objects.filter(solicitud=solicitud).delete()
        nuevo_certificado = Certificado.objects.create(
            solicitud=solicitud,
            codigo_certificado=codigo_certificado,
            fecha_vencimiento=fecha_vencimiento
        )
        # Aquí guardaríamos el archivo físico, pero para este ejemplo, lo servimos directamente.
        # En un caso real, guardarías `pdf` en `nuevo_certificado.archivo_pdf`.

        # 6. Devolver el PDF como una respuesta HTTP para descargar
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="certificado_{solicitud.empresa.nit}.pdf"'
        return response
    
class ExpedienteHistorialView(StaffRequiredMixin, DetailView):
    model = Solicitud
    template_name = 'staff_panel/expediente_historial.html'
    context_object_name = 'solicitud'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtenemos el "tipo de contenido" del modelo Solicitud
        solicitud_type = ContentType.objects.get_for_model(self.object)
        # Filtramos el log de auditoría para mostrar solo los registros de esta solicitud específica
        context['historial'] = Auditoria.objects.filter(
            content_type=solicitud_type,
            object_id=self.object.pk
        )
        return context
    
class IncidenciaListView(DirectorRequiredMixin, ListView):
    model = Incidencia
    template_name = 'staff_panel/incidencia_list.html'
    context_object_name = 'incidencias'
    ordering = ['-fecha_reporte']

class IncidenciaCreateView(DirectorRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        solicitud = get_object_or_404(Solicitud, pk=kwargs['solicitud_pk'])
        form = IncidenciaForm()
        return render(request, 'staff_panel/incidencia_form.html', {'form': form, 'solicitud': solicitud})

    def post(self, request, *args, **kwargs):
        solicitud = get_object_or_404(Solicitud, pk=kwargs['solicitud_pk'])
        form = IncidenciaForm(request.POST, request.FILES)
        if form.is_valid():
            incidencia = form.save(commit=False)
            incidencia.solicitud = solicitud
            incidencia.registrado_por = request.user
            incidencia.save()
            registrar_auditoria(request.user, solicitud, f"Se registró una nueva incidencia: '{incidencia.get_tipo_display()}'.")
            messages.success(request, 'Incidencia registrada correctamente.')
            return redirect('incidencia_list')
        return render(request, 'staff_panel/incidencia_form.html', {'form': form, 'solicitud': solicitud})

class IncidenciaUpdateView(DirectorRequiredMixin, UpdateView):
    model = Incidencia
    form_class = IncidenciaForm
    template_name = 'staff_panel/incidencia_form.html'
    success_url = reverse_lazy('incidencia_list')

    def form_valid(self, form):
        incidencia = form.save()
        registrar_auditoria(self.request.user, incidencia.solicitud, f"Se actualizó la incidencia '{incidencia.get_tipo_display()}'. Nuevo estado: {incidencia.estado}.")
        messages.success(self.request, 'Incidencia actualizada.')
        return super().form_valid(form)
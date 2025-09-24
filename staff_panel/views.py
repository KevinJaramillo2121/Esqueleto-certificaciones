# staff_panel/views.py
from django.shortcuts import render
from django.views import View
from users.mixins import StaffRequiredMixin # <-- Importamos nuestro mixin
from expedientes.models import Solicitud
from .forms import AlcanceRevisionFormSet # <-- Importamos nuestro FormSet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


class StaffDashboardView(StaffRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Filtramos las solicitudes que están "En Revisión"
        solicitudes_por_revisar = Solicitud.objects.filter(estado='En Revisión').order_by('fecha_creacion')

        context = {
            'solicitudes_por_revisar': solicitudes_por_revisar,
            # Aquí añadiremos más queries a medida que el flujo crezca
        }
        return render(request, 'staff_panel/staff_dashboard.html', context)

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
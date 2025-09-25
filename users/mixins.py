# users/mixins.py
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.contrib import messages


class StaffRequiredMixin(AccessMixin):
    """
    Verifica que el usuario actual haya iniciado sesión y sea personal (staff).
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_staff:
            messages.error(request, "No tienes permiso para acceder a esta página.")
            return redirect('dashboard') # Redirige al dashboard del cliente
        return super().dispatch(request, *args, **kwargs)

class EvaluadorRequiredMixin(AccessMixin):
    """
    Verifica que el usuario actual haya iniciado sesión y tenga un perfil de evaluador.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        # Usamos hasattr para comprobar si el atributo 'perfil_evaluador' existe
        if not hasattr(request.user, 'perfil_evaluador'):
            messages.error(request, "No tienes permiso para acceder a esta página.")
            return redirect('staff_dashboard') # O a la página de login
        return super().dispatch(request, *args, **kwargs)

class RevisorRequiredMixin(AccessMixin):
    """
    Verifica que el usuario actual haya iniciado sesión y tenga el rol de Revisor o Director.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        # Un Director también puede actuar como Revisor.
        if not (request.user.rol.nombre == 'Revisor' or request.user.rol.nombre == 'Director de Certificaciones'):
            messages.error(request, "No tienes permiso para acceder a esta página.")
            return redirect('staff_dashboard') # Redirige al panel principal del staff
        return super().dispatch(request, *args, **kwargs)
    
class DirectorRequiredMixin(AccessMixin):
    """
    Verifica que el usuario actual haya iniciado sesión y tenga el rol de Director.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.rol or request.user.rol.nombre != 'Director de Certificaciones':
            messages.error(request, "Solo el Director de Certificaciones puede realizar esta acción.")
            return redirect('staff_dashboard')
        return super().dispatch(request, *args, **kwargs)

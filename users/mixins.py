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

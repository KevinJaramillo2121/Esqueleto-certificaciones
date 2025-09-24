from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView # <-- Importa LoginView
from django.shortcuts import redirect

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login') # Redirige al login tras un registro exitoso
    template_name = 'registration/signup.html'

class CustomLoginView(LoginView):
    def form_valid(self, form):
        """
        Sobrescribimos este método para redirigir al usuario según su tipo.
        """
        super().form_valid(form) # Primero, autentica al usuario
        
        # Ahora, comprobamos si es 'staff'
        if self.request.user.is_staff:
            return redirect('staff_dashboard') # Redirige al panel de staff
        else:
            return redirect('dashboard') # Redirige al dashboard de cliente

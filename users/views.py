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
        super().form_valid(form)
        
        # AÑADIMOS ESTA LÓGICA
        if hasattr(self.request.user, 'perfil_evaluador'):
            return redirect('evaluador_dashboard')
        
        if self.request.user.is_staff:
            return redirect('staff_dashboard')
        else:
            return redirect('dashboard')

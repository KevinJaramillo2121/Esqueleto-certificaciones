# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('email', 'nombre', 'apellido') # Campos que aparecerán en el formulario

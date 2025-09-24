# expedientes/forms.py
from django import forms
from .models import Empresa

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        # Excluimos el campo 'usuario' porque lo asignaremos automáticamente en la vista.
        fields = [
            'nit', 'razon_social', 'pais', 'departamento', 'municipio',
            'correo_principal', 'telefono_fijo', 'telefono_movil'
        ]

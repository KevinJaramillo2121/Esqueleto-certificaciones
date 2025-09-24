# expedientes/forms.py
from django import forms
from .models import Empresa, Sede, RepresentanteLegal

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        # Excluimos el campo 'usuario' porque lo asignaremos automáticamente en la vista.
        fields = [
            'nit', 'razon_social', 'pais', 'departamento', 'municipio',
            'correo_principal', 'telefono_fijo', 'telefono_movil'
        ]

class SedeForm(forms.ModelForm):
    class Meta:
        model = Sede
        # Excluimos 'empresa' porque la asignaremos en la vista
        fields = ['direccion', 'pais', 'departamento', 'municipio']

class RepresentanteLegalForm(forms.ModelForm):
    class Meta:
        model = RepresentanteLegal
        # Incluimos todos los campos que el usuario debe llenar.
        # Excluimos 'empresa' porque la asignaremos automáticamente.
        fields = [
            'tipo_documento', 'numero_documento', 'nombres', 'apellidos',
            'correo_personal', 'telefono_movil', 'documento_pdf'
        ]

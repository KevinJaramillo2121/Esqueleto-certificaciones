# staff_panel/forms.py
from django import forms
from expedientes.models import Solicitud, Alcance, Evaluador, Actividad, Evidencia


# Este es el formulario para cada fila (cada alcance)
class AlcanceRevisionForm(forms.ModelForm):
    class Meta:
        model = Alcance
        fields = ['revision_conforme', 'revision_observaciones']
        widgets = {
            'revision_conforme': forms.Select(choices=[
                (None, '---'),
                (True, 'Conforme'),
                (False, 'No Conforme')
            ]),
            'revision_observaciones': forms.Textarea(attrs={'rows': 2}),
        }

# Este es el "factory" que crea un conjunto de formularios de Alcance
# vinculados a una Solicitud. `extra=0` significa que no mostrará formularios vacíos extra.
AlcanceRevisionFormSet = forms.inlineformset_factory(
    Solicitud,
    Alcance,
    form=AlcanceRevisionForm,
    extra=0,
    can_delete=False
)


class EvaluadorForm(forms.ModelForm):
    class Meta:
        model = Evaluador
        fields = ['nombres', 'apellidos', 'correo', 'telefono', 'costo_dia', 'campo_accion']

ActividadFormSet = forms.inlineformset_factory(
    Solicitud,      # Modelo Padre
    Actividad,      # Modelo Hijo
    fields=('nombre', 'evaluador_asignado', 'fecha_inicio_planificada', 'dias_planificados', 'fecha_limite_evidencias'),
    extra=1,        # Muestra 1 formulario vacío por defecto
    can_delete=True
)

class EvidenciaForm(forms.ModelForm):
    class Meta:
        model = Evidencia
        fields = ['archivo', 'descripcion']
        # Hacemos que la descripción sea opcional
        widgets = {
            'descripcion': forms.TextInput(attrs={'placeholder': 'Ej: Acta de reunión, Informe de laboratorio, etc.'}),
        }


class EvidenciaRevisionForm(forms.ModelForm):
    class Meta:
        model = Evidencia
        # Solo exponemos los campos de revisión
        fields = ['revision_conforme', 'revision_observaciones']
        widgets = {
            'revision_conforme': forms.Select(choices=[
                (None, '---'),
                (True, 'Conforme'),
                (False, 'No Conforme')
            ]),
            'revision_observaciones': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Añadir observación si no es conforme...'}),
        }

# Creamos un FormSet basado en el modelo, no anidado.
EvidenciaRevisionFormSet = forms.modelformset_factory(
    Evidencia,
    form=EvidenciaRevisionForm,
    extra=0  # No mostrar formularios vacíos extra
)
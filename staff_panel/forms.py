# staff_panel/forms.py
from django import forms
from expedientes.models import Solicitud, Alcance

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

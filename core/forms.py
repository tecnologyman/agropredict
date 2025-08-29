# core/forms.py
from django import forms
from .models import Prediccion
from .cl_geo import REGIONES, COMUNAS_POR_REGION, ALL_COMUNAS_CHOICES

# En la UI hablamos de especie (manzano/cerezo)
ESPECIE_CHOICES = (
    ("MANZANO", "Manzano"),
    ("CEREZO", "Cerezo"),
)

# Sistemas de riego demo
RIEGO_CHOICES = (
    ("GOTEO", "Goteo"),
    ("ASPERSION", "Aspersión"),
    ("SURCO", "Surco"),
)

def _region_choices():
    """
    Asegura un shape correcto para choices:
    - Si REGIONES es ['Valparaíso', ...] -> [('Valparaíso','Valparaíso'), ...]
    - Si ya viene como tuplas -> lo respeta.
    """
    if REGIONES and isinstance(REGIONES[0], (list, tuple)) and len(REGIONES[0]) == 2:
        return REGIONES
    return [(r, r) for r in REGIONES]

class PrediccionForm(forms.ModelForm):
    # Declaramos explícitamente TODOS los campos que usa la vista
    especie = forms.ChoiceField(choices=ESPECIE_CHOICES)

    region = forms.ChoiceField(
        choices=_region_choices(),
        widget=forms.Select(attrs={"id": "id_region"})
    )

    # Partimos con placeholder; se rellenará por JS y/o __init__
    comuna = forms.ChoiceField(
        choices=[("", "— Selecciona comuna —")] + ALL_COMUNAS_CHOICES,
        widget=forms.Select(attrs={"id": "id_comuna"})
    )

    superficie_ha = forms.FloatField(
        min_value=0,
        widget=forms.NumberInput(attrs={"step": "0.01"})
    )

    edad_arbol_anios = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={"min": "0"})
    )

    densidad_arboles_ha = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={"min": "0"})
    )

    sistema_riego = forms.ChoiceField(choices=RIEGO_CHOICES)

    class Meta:
        model = Prediccion
        fields = [
            "especie",
            "region",
            "comuna",
            "superficie_ha",
            "edad_arbol_anios",
            "densidad_arboles_ha",
            "sistema_riego",
        ]

    def __init__(self, *args, **kwargs):
        """
        Si hay región (en POST/GET o en instancia), limitamos las comunas.
        Además preservamos una comuna existente aunque no esté en el catálogo
        para evitar que se 'pierda' al editar registros antiguos.
        """
        super().__init__(*args, **kwargs)

        # Tomamos región desde data (POST/GET) o desde la instancia (edición)
        reg = self.data.get("region") or getattr(self.instance, "region", "")
        if reg:
            comunas = COMUNAS_POR_REGION.get(reg, [])
            if comunas:
                self.fields["comuna"].choices = [("", "— Selecciona comuna —")] + [(c, c) for c in comunas]

            # Si hay comuna existente (data o instancia) que no esté en el catálogo actual, la preservamos
            existente = self.data.get("comuna") or getattr(self.instance, "comuna", "")
            if existente and existente not in dict(self.fields["comuna"].choices):
                self.fields["comuna"].choices = [(existente, existente)] + list(self.fields["comuna"].choices)

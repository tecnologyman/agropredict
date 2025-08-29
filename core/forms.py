# core/forms.py
from django import forms
from .models import Prediccion
from .cl_geo import REGIONES, COMUNAS_POR_REGION, ALL_COMUNAS_CHOICES


class PrediccionForm(forms.ModelForm):
    region = forms.ChoiceField(choices=REGIONES)
    # Por defecto muestra todas las comunas (para no dejarlo vacío si cambia región vía JS)
    comuna = forms.ChoiceField(choices=[("", "— Selecciona región —")] + ALL_COMUNAS_CHOICES)

    class Meta:
        model = Prediccion
        fields = [
            "especie",
            "region", "comuna",
            "superficie_ha",
            "edad_arbol_anios",
            "densidad_arboles_ha",
            "sistema_riego",
        ]
        widgets = {
            "region": forms.Select(attrs={"id": "id_region", "class": "input"}),
            "comuna": forms.Select(attrs={"id": "id_comuna", "class": "input"}),
            "especie": forms.Select(attrs={"class": "input"}),
            "superficie_ha": forms.NumberInput(attrs={"class": "input", "step": "0.01", "min": "0"}),
            "edad_arbol_anios": forms.NumberInput(attrs={"class": "input", "min": "0", "step": "1"}),
            "densidad_arboles_ha": forms.NumberInput(attrs={"class": "input", "min": "1", "step": "1"}),
            "sistema_riego": forms.Select(attrs={"class": "input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si viene región (GET/POST/instance), limita comunas
        reg = self.data.get("region") or getattr(self.instance, "region", "")
        if reg:
            comunas = COMUNAS_POR_REGION.get(reg, [])
            if comunas:
                self.fields["comuna"].choices = [(c, c) for c in comunas]
            existente = self.data.get("comuna") or getattr(self.instance, "comuna", "")
            if existente and existente not in comunas:
                self.fields["comuna"].choices = [(existente, existente)] + self.fields["comuna"].choices

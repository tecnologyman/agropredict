from django import forms
from .models import Prediccion, FRUTAL_CHOICES, REGIONES

class PrediccionForm(forms.ModelForm):
    arbol_frutal = forms.ChoiceField(choices=FRUTAL_CHOICES, label='Árbol frutal')
    region = forms.ChoiceField(choices=REGIONES, label='Región')

    class Meta:
        model = Prediccion
        fields = ['region','arbol_frutal','superficie_ha','temp_prom_anual_c','precip_anual_mm','radiacion_anual_wm2']
        labels = {
            'superficie_ha':'Superficie Plantada (ha)',
            'temp_prom_anual_c':'Temp. Prom. Anual (°C)',
            'precip_anual_mm':'Precip. Anual (mm)',
            'radiacion_anual_wm2':'Radiación Anual (W/m²)',
        }
        widgets = {
            'region': forms.Select(attrs={'class':'input', 'id':'id_region'}),
            'arbol_frutal': forms.Select(attrs={'class':'input', 'id':'id_arbol_frutal'}),
            'superficie_ha': forms.NumberInput(attrs={'step':'0.01','class':'input'}),
            'temp_prom_anual_c': forms.NumberInput(attrs={'step':'0.1','class':'input'}),
            'precip_anual_mm': forms.NumberInput(attrs={'step':'0.1','class':'input'}),
            'radiacion_anual_wm2': forms.NumberInput(attrs={'step':'0.1','class':'input'}),
        }

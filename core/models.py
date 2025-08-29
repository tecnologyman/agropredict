from django.conf import settings
from django.db import models

REGIONES = [
    ('Arica y Parinacota','Arica y Parinacota'),
    ('Tarapacá','Tarapacá'),
    ('Antofagasta','Antofagasta'),
    ('Atacama','Atacama'),
    ('Coquimbo','Coquimbo'),
    ('Valparaíso','Valparaíso'),
    ('Metropolitana','Metropolitana'),
    ('O’Higgins','O’Higgins'),
    ('Maule','Maule'),
    ('Ñuble','Ñuble'),
    ('Biobío','Biobío'),
    ('La Araucanía','La Araucanía'),
    ('Los Ríos','Los Ríos'),
    ('Los Lagos','Los Lagos'),
    ('Aysén','Aysén'),
    ('Magallanes','Magallanes'),
]

FRUTAL_CHOICES = [('manzana','Manzana'), ('cereza','Cereza')]

class Prediccion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    region = models.CharField(max_length=40, choices=REGIONES)
    arbol_frutal = models.CharField(max_length=16, choices=FRUTAL_CHOICES, default='manzana')
    superficie_ha = models.FloatField()
    temp_prom_anual_c = models.FloatField()
    precip_anual_mm = models.FloatField()
    radiacion_anual_wm2 = models.FloatField()
    produccion_esperada_t = models.FloatField()
    proyeccion_json = models.TextField(help_text='JSON de 5 periodos')
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado']

    def __str__(self):
        return f'Predicción #{self.pk} · {self.get_arbol_frutal_display()} · {self.region}'

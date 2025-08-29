from django.conf import settings
from django.db import models

REGIONES = [
<<<<<<< HEAD
    ("Arica y Parinacota","Arica y Parinacota"),
    ("Tarapacá","Tarapacá"),
    ("Antofagasta","Antofagasta"),
    ("Atacama","Atacama"),
    ("Coquimbo","Coquimbo"),
    ("Valparaíso","Valparaíso"),
    ("Metropolitana","Metropolitana"),
    ("O’Higgins","O’Higgins"),
    ("Maule","Maule"),
    ("Ñuble","Ñuble"),
    ("Biobío","Biobío"),
    ("La Araucanía","La Araucanía"),
    ("Los Ríos","Los Ríos"),
    ("Los Lagos","Los Lagos"),
    ("Aysén","Aysén"),
    ("Magallanes","Magallanes"),
]

ESPECIES = [
    ("MANZANO","Manzano"),
    ("CEREZO","Cerezo"),
]

SISTEMA_RIEGO = [
    ("GOTEO","Goteo"),
    ("ASPERSION","Aspersión"),
    ("SURCO","Surco"),
]

class Prediccion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    especie = models.CharField(max_length=16, choices=ESPECIES, default="MANZANO")

    region = models.CharField(max_length=32, choices=REGIONES)
    comuna = models.CharField(max_length=64)  # dependiente de región

    superficie_ha = models.FloatField()
    edad_arbol_anios = models.PositiveIntegerField()
    densidad_arboles_ha = models.PositiveIntegerField()
    sistema_riego = models.CharField(max_length=12, choices=SISTEMA_RIEGO, default="GOTEO")

    # Campos climáticos antiguos -> opcionales (quedan por compatibilidad, no se usan en el form)
    temp_prom_anual_c = models.FloatField(null=True, blank=True)
    precip_anual_mm = models.FloatField(null=True, blank=True)
    radiacion_anual_wm2 = models.FloatField(null=True, blank=True)

    produccion_esperada_t = models.FloatField()
    proyeccion_json = models.TextField()  # lista de 5 (semestral)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pred #{self.pk} · {self.get_especie_display()} · {self.comuna}, {self.region}"
=======
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
>>>>>>> 1929edb89119ee1b7292b948c6f40e50284b9889

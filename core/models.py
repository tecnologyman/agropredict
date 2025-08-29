# core/models.py
from django.conf import settings
from django.db import models


class Prediccion(models.Model):
    ESPECIE_CHOICES = [
        ("MANZANO", "Manzano"),
        ("CEREZO", "Cerezo"),
    ]
    RIEGO_CHOICES = [
        ("GOTEO", "Goteo"),
        ("ASPERSION", "Aspersión"),
        ("SURCO", "Surco"),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="predicciones")

    especie = models.CharField(max_length=20, choices=ESPECIE_CHOICES, default="MANZANO")
    region = models.CharField(max_length=60)
    comuna = models.CharField(max_length=80)

    superficie_ha = models.DecimalField(max_digits=10, decimal_places=2)
    edad_arbol_anios = models.PositiveIntegerField()
    densidad_arboles_ha = models.PositiveIntegerField()
    sistema_riego = models.CharField(max_length=20, choices=RIEGO_CHOICES, default="SURCO")

    produccion_esperada_t = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    proyeccion_json = models.TextField(blank=True, default="")

    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado"]

    def __str__(self):
        return f"Predicción #{self.pk} · {self.get_especie_display()} · {self.comuna}, {self.region}"

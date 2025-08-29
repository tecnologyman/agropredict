from django.contrib import admin
from .models import Prediccion

@admin.register(Prediccion)
class PredAdmin(admin.ModelAdmin):
    list_display = ("id","usuario","especie","comuna","region","superficie_ha","edad_arbol_anios","densidad_arboles_ha","sistema_riego","produccion_esperada_t","creado")
    list_filter = ("especie","region","sistema_riego","creado")
    search_fields = ("comuna","region","usuario__username")

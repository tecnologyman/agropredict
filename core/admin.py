# core/admin.py
from django.contrib import admin
from .models import Prediccion

@admin.register(Prediccion)
class PrediccionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario",
        "especie",                # <— antes era arbol_frutal
        "region",
        "comuna",
        "superficie_ha",
        "produccion_esperada_t",
        "creado",
    )
    list_filter = (
        "especie",                # <— antes era arbol_frutal
        "region",
        "comuna",
        "sistema_riego",
        "creado",
    )
    search_fields = ("region", "comuna", "usuario__username")
    ordering = ("-creado",)
    date_hierarchy = "creado"

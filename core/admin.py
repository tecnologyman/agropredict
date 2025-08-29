from django.contrib import admin
from .models import Prediccion

@admin.register(Prediccion)
<<<<<<< HEAD
class PredAdmin(admin.ModelAdmin):
    list_display = ("id","usuario","especie","comuna","region","superficie_ha","edad_arbol_anios","densidad_arboles_ha","sistema_riego","produccion_esperada_t","creado")
    list_filter = ("especie","region","sistema_riego","creado")
    search_fields = ("comuna","region","usuario__username")
=======
class PrediccionAdmin(admin.ModelAdmin):
    list_display = ('id','usuario','arbol_frutal','region','produccion_esperada_t','creado')
    list_filter = ('arbol_frutal','region','usuario','creado')
    search_fields = ('usuario__username','region')
>>>>>>> 1929edb89119ee1b7292b948c6f40e50284b9889

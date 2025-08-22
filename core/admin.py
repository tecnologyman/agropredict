from django.contrib import admin
from .models import Prediccion

@admin.register(Prediccion)
class PrediccionAdmin(admin.ModelAdmin):
    list_display = ('id','usuario','arbol_frutal','region','produccion_esperada_t','creado')
    list_filter = ('arbol_frutal','region','usuario','creado')
    search_fields = ('usuario__username','region')

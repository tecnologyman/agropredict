# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("prediccion/", views.prediccion_form, name="prediccion_form"),
    path("prediccion/<int:pk>/", views.prediccion_resultado, name="prediccion_resultado"),
    path("api/comunas/<slug:region_slug_value>/", views.comunas_api, name="comunas_api"),
]

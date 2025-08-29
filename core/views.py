# core/views.py
# -*- coding: utf-8 -*-
import json
import statistics
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.utils import OperationalError, ProgrammingError
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .forms import PrediccionForm
from .models import Prediccion
from .cl_geo import COMUNAS_POR_REGION, region_slug

# ----------------------
# Parámetros de la demo
# ----------------------
RIEGO_FACTOR = {"GOTEO": 1.10, "ASPERSION": 1.05, "SURCO": 1.00}
COMUNA_FACTOR = {
    "Quillota": 1.06, "Los Andes": 1.05, "San Antonio": 0.97, "Viña del Mar": 0.98,
}


def _baseline(superficie, especie, edad, densidad, riego, comuna):
    """
    Baseline explicable:
    - base = 0.8 * superficie
    - edad: rampa 0.5 → 1.0 a los 5 años
    - densidad: óptimo 800 árboles/ha, penaliza hasta -12%
    - riego: goteo +10%, aspersión +5%
    - comuna: ajustes leves demo
    - especie: cerezo +4% (demo)
    """
    base = 0.8 * (float(superficie or 0))

    factor_edad = max(0.5, min((edad or 0) / 5.0, 1.0))
    dens_penalty = min(abs((densidad or 0) - 800) / 800.0, 0.3) * 0.4
    factor_densidad = 1.0 - dens_penalty
    factor_riego = RIEGO_FACTOR.get(riego, 1.0)
    factor_comuna = COMUNA_FACTOR.get(comuna, 1.0)
    factor_especie = 1.04 if especie == "CEREZO" else 1.00

    produccion = base * factor_edad * factor_densidad * factor_riego * factor_comuna * factor_especie
    produccion = max(0, round(produccion, 2))

    # Semestral: 5 puntos +5% incremental
    proy_sem = [round(produccion * (1 + i * 0.05), 2) for i in range(5)]
    # Anual: 3 años, 8% acumulativo
    proy_anual = [round(produccion * ((1.08) ** (i + 1)), 2) for i in range(3)]
    return produccion, proy_sem, proy_anual


# ----------------------
# Dashboard
# ----------------------
@login_required
def dashboard(request):
    try:
        predicciones = (
            Prediccion.objects
            .filter(usuario=request.user)
            .order_by('-creado')[:5]
        )
    except (OperationalError, ProgrammingError):
        predicciones = []

    # t/ha seguro + serie para el gráfico
    serie_vals, serie_labels = [], []
    for p in reversed(list(predicciones)):  # ascendente en el tiempo
        if p.superficie_ha:
            try:
                p.t_por_ha = round((float(p.produccion_esperada_t or 0)) / float(p.superficie_ha), 2)
            except (TypeError, ValueError, ZeroDivisionError):
                p.t_por_ha = None
        else:
            p.t_por_ha = None

        if p.produccion_esperada_t is not None:
            serie_vals.append(float(p.produccion_esperada_t))
            especie = p.get_especie_display() if hasattr(p, "get_especie_display") else (p.especie or "")
            serie_labels.append(f"#{p.id} · {especie} · {float(p.produccion_esperada_t):.2f} t")

    # Puntos SVG del gráfico
    width, height = 1100, 260
    left, right, top, bottom = 50, 20, 20, 30
    usable_w = width - left - right
    usable_h = height - top - bottom

    if serie_vals:
        vmax = max(serie_vals)
        vmin = min(serie_vals)
        span = (vmax - vmin) or 1.0
        n = len(serie_vals)
        pts = []
        for i, val in enumerate(serie_vals):
            x = left + (usable_w * (i / (n - 1 if n > 1 else 1)))
            y = top + usable_h * (1 - ((val - vmin) / span))
            pts.append(f"{x:.0f},{y:.0f}")
        chart_points = " ".join(pts)
    else:
        vmin, vmax, chart_points = 0, 1, ""

    # Posiciones de cuadrícula vertical (para no hacer aritmética en el template)
    grid_x_positions = []
    grid_cols = 4
    step = usable_w / float(grid_cols)
    for i in range(1, grid_cols + 1):
        grid_x_positions.append(int(round(left + step * i)))

    # KPIs demo
    kpi_et0 = 5.1
    kpi_precip_7d = 24
    kpi_ventana_riego = "Alta prob."
    t_ha_vals = [p.t_por_ha for p in predicciones if p.t_por_ha is not None]
    if t_ha_vals:
        prom_t_ha = statistics.mean(t_ha_vals)
        if prom_t_ha >= 1.2:
            kpi_riesgo = "Bajo"
        elif prom_t_ha >= 0.8:
            kpi_riesgo = "Medio"
        else:
            kpi_riesgo = "Alto"
    else:
        kpi_riesgo = "Medio"

    ctx = {
        "predicciones": predicciones,
        "chart_points": chart_points,
        "chart_labels": serie_labels,
        "chart_has_data": bool(serie_vals),
        "grid_x_positions": grid_x_positions,
        "kpi_riesgo": kpi_riesgo,
        "kpi_et0": kpi_et0,
        "kpi_ventana_riego": kpi_ventana_riego,
        "kpi_precip_7d": kpi_precip_7d,
    }
    return render(request, "core/dashboard.html", ctx)


# ----------------------
# Crear predicción
# ----------------------
@login_required
def prediccion_form(request):
    if request.method == "POST":
        form = PrediccionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            prod, proy_sem, proy_anual = _baseline(
                data["superficie_ha"],
                data["especie"],
                data["edad_arbol_anios"],
                data["densidad_arboles_ha"],
                data["sistema_riego"],
                data["comuna"],
            )
            p = Prediccion.objects.create(
                usuario=request.user,
                especie=data["especie"],
                region=data["region"],
                comuna=data["comuna"],
                superficie_ha=data["superficie_ha"],
                edad_arbol_anios=data["edad_arbol_anios"],
                densidad_arboles_ha=data["densidad_arboles_ha"],
                sistema_riego=data["sistema_riego"],
                produccion_esperada_t=prod,
                proyeccion_json=json.dumps({"semestral": proy_sem, "anual": proy_anual}),
            )
            return redirect("prediccion_resultado", pk=p.pk)
    else:
        form = PrediccionForm()
    return render(request, "core/prediccion_form.html", {"form": form})


# ----------------------
# Ver/editar resultado
# ----------------------
@login_required
def prediccion_resultado(request, pk):
    p = get_object_or_404(Prediccion, pk=pk, usuario=request.user)

    if request.method == "POST":
        form = PrediccionForm(request.POST, instance=p)
        if form.is_valid():
            p = form.save(commit=False)
            prod, proy_sem, proy_anual = _baseline(
                p.superficie_ha, p.especie, p.edad_arbol_anios,
                p.densidad_arboles_ha, p.sistema_riego, p.comuna
            )
            p.produccion_esperada_t = prod
            p.proyeccion_json = json.dumps({"semestral": proy_sem, "anual": proy_anual})
            p.save()
            return redirect("prediccion_resultado", pk=p.pk)
    else:
        form = PrediccionForm(instance=p)

    proy = json.loads(p.proyeccion_json) if p.proyeccion_json else {"semestral": [], "anual": []}
    proy_sem = proy.get("semestral", [])
    proy_anual = proy.get("anual", [])

    # Puntos SVG (serie semestral)
    seq = proy_sem or []
    max_v = max(seq) if seq else 1
    min_v = min(seq) if seq else 0
    span = (max_v - min_v) or 1
    width, height = 700, 200
    left, right, top, bottom = 40, 20, 20, 20
    usable_w = width - left - right
    usable_h = height - top - bottom
    pts = []
    if seq:
        for i, val in enumerate(seq):
            x = left + (usable_w * i / (len(seq) - 1 if len(seq) > 1 else 1))
            y = top + usable_h * (1 - ((val - min_v) / span))
            pts.append(f"{x:.0f},{y:.0f}")
    points_str = " ".join(pts)

    prod_por_ha = round(float(p.produccion_esperada_t or 0) / float(p.superficie_ha or 1), 2) if p.superficie_ha else 0

    ctx = {
        "p": p,
        "form_edit": form,
        "proy_sem": proy_sem,
        "proy_anual": proy_anual,
        "points": points_str,
        "min_v": min_v,
        "max_v": max_v,
        "prod_por_ha": prod_por_ha,
    }
    return render(request, "core/prediccion_resultado.html", ctx)


# ----------------------
# API comunas por región
# ----------------------
@require_GET
@login_required
def comunas_api(request, region_slug_value):
    # Busca el nombre de región real a partir del slug
    region_name = next((r for r in COMUNAS_POR_REGION.keys() if region_slug(r) == region_slug_value), None)
    comunas = COMUNAS_POR_REGION.get(region_name, [])
    return JsonResponse({"region": region_name, "comunas": comunas})

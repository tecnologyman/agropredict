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

# ======================
# Parámetros de la demo
# ======================

# Incrementos por sistema de riego (explicable)
RIEGO_FACTOR = {
    "GOTEO": 1.10,
    "ASPERSION": 1.05,
    "SURCO": 1.00,
}

# Ajuste por comuna (demo simple): interior ↑, costa ↓
COMUNA_FACTOR = {
    "Quillota": 1.06,
    "Los Andes": 1.05,
    "San Antonio": 0.97,
    "Viña del Mar": 0.98,
}

# ======================
# Cálculo "baseline"
# ======================

def _baseline(superficie, especie, edad, densidad, riego, comuna):
    """
    Baseline explicable para Sprint 1 (sin dependencias externas):

    - base = 0.8 * superficie
    - factor_edad: rampa 0.5 (árbol joven) → 1.0 a partir de 5 años
          factor_edad = clamp(edad/5, 0.5, 1.0)
    - factor_densidad: óptimo 800 árboles/ha (penaliza suavemente hasta -12%)
          dens_penalty = min(|densidad - 800| / 800, 0.3) * 0.4
          factor_densidad = 1 - dens_penalty
    - factor_riego: goteo +10%, aspersión +5%, surco 0%
    - factor_comuna: pequeño ajuste si está en tabla (default 1.0)
    - factor_especie: cerezo (CEREZO) levemente mayor en esta demo (+4%)
    """
    base = 0.8 * (superficie or 0)

    factor_edad = max(0.5, min((edad or 0) / 5.0, 1.0))
    dens_penalty = min(abs((densidad or 0) - 800) / 800.0, 0.3) * 0.4
    factor_densidad = 1.0 - dens_penalty
    factor_riego = RIEGO_FACTOR.get(riego, 1.0)
    factor_comuna = COMUNA_FACTOR.get(comuna, 1.0)
    factor_especie = 1.04 if especie == "CEREZO" else 1.00  # MANZANO = 1.00

    produccion = base * factor_edad * factor_densidad * factor_riego * factor_comuna * factor_especie
    produccion = max(0, round(produccion, 2))

    # Proyección semestral (5 periodos) +5% incremental por periodo
    proy_sem = [round(produccion * (1 + i * 0.05), 2) for i in range(5)]

    # Proyección anual (3 años) con 8% acumulativo
    proy_anual = [round(produccion * ((1.08) ** (i + 1)), 2) for i in range(3)]

    return produccion, proy_sem, proy_anual


# ======================
# Dashboard
# ======================

@login_required
def dashboard(request):
    # 1) Trae últimas 5 predicciones del usuario
    try:
        predicciones = (
            Prediccion.objects
            .filter(usuario=request.user)
            .order_by('-creado')[:5]
        )
    except (OperationalError, ProgrammingError):
        predicciones = []

    # 2) Calcula t/ha seguro y prepara serie para el gráfico
    serie_vals = []     # valores (t) en orden cronológico
    serie_labels = []   # etiquetas para leyenda
    cards = []
    for p in reversed(list(predicciones)):   # ascendente en el tiempo
        # t/ha robusto (evita excepción por strings localizados)
        try:
            sup = float(p.superficie_ha) if p.superficie_ha is not None else 0.0
        except (TypeError, ValueError):
            sup = 0.0

        if sup > 0:
            try:
                t_ha = round(float(p.produccion_esperada_t or 0) / sup, 2)
            except (TypeError, ValueError):
                t_ha = None
        else:
            t_ha = None

        # lo guardamos para tarjetas
        p.t_por_ha = t_ha
        cards.append(p)

        # valores para el gráfico (usamos producción total t)
        if p.produccion_esperada_t is not None:
            try:
                val = float(p.produccion_esperada_t)
            except (TypeError, ValueError):
                val = None
            if val is not None:
                serie_vals.append(val)
                especie = p.get_especie_display() if hasattr(p, "get_especie_display") else (p.especie or "")
                serie_labels.append(f"#{p.id} · {especie} · {val:.2f} t")

    # 3) Construye puntos SVG (sin aritmética en el template)
    width, height = 1100, 260
    left, right, top, bottom = 50, 20, 20, 30
    usable_w = width - left - right
    usable_h = height - top - bottom
    x_min = left
    x_max = left + usable_w
    y_base = top + usable_h  # 230

    if serie_vals:
        vmax = max(serie_vals)
        vmin = min(serie_vals)
        span = (vmax - vmin) or 1.0
        n = len(serie_vals)
        pts_xy = []
        for i, val in enumerate(serie_vals):
            x = left + (usable_w * (i / (n - 1 if n > 1 else 1)))
            y = top + usable_h * (1 - ((val - vmin) / span))
            pts_xy.append((round(x), round(y)))
        chart_points = " ".join(f"{x},{y}" for x, y in pts_xy)
        chart_points_xy = pts_xy
    else:
        vmin, vmax = 0.0, 1.0
        chart_points = ""
        chart_points_xy = []

    # Área bajo la curva (relleno agradable)
    chart_fill_points = f"{chart_points} {x_max},{y_base} {x_min},{y_base}" if chart_points else ""

    # Cuadrícula vertical (4 separadores internos; posiciones ya calculadas)
    grid_xs = [round(left + usable_w * (k / 5.0)) for k in (1, 2, 3, 4)]

    # 4) KPI demo (valores estáticos/derivados para Sprint 1)
    kpi_et0 = 5.1
    kpi_precip_7d = 24
    kpi_ventana_riego = "Alta prob."
    # Riesgo “demo”: simple en función del promedio de t/ha si existe
    t_ha_vals = [p.t_por_ha for p in cards if p.t_por_ha is not None]
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
        "predicciones": list(reversed(cards)),   # para que se vean de más reciente a más antigua en la lista
        # Chart
        "chart_points": chart_points,
        "chart_points_xy": chart_points_xy,   # por si quieres pintar círculos
        "chart_fill_points": chart_fill_points,
        "chart_min": vmin,
        "chart_max": vmax,
        "chart_labels": serie_labels,
        "chart_has_data": bool(chart_points),
        "grid_xs": grid_xs,
        "x_min": x_min,
        "x_max": x_max,
        "y_top": top,
        "y_base": y_base,
        # KPI
        "kpi_riesgo": kpi_riesgo,
        "kpi_et0": kpi_et0,
        "kpi_ventana_riego": kpi_ventana_riego,
        "kpi_precip_7d": kpi_precip_7d,
    }
    return render(request, "core/dashboard.html", ctx)


# ======================
# Crear predicción
# ======================

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


# ======================
# Ver/editar resultado
# ======================

@login_required
def prediccion_resultado(request, pk):
    p = get_object_or_404(Prediccion, pk=pk, usuario=request.user)

    # Edición rápida en la misma página
    if request.method == "POST":
        form = PrediccionForm(request.POST, instance=p)
        if form.is_valid():
            p = form.save(commit=False)
            prod, proy_sem, proy_anual = _baseline(
                p.superficie_ha,
                p.especie,
                p.edad_arbol_anios,
                p.densidad_arboles_ha,
                p.sistema_riego,
                p.comuna,
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

    # Preparar puntos para gráfico SVG (serie semestral)
    seq = proy_sem
    max_v = max(seq) if seq else 1
    min_v = min(seq) if seq else 0
    span = (max_v - min_v) or 1
    width, height = 700, 200
    left, right, top, bottom = 40, 20, 20, 20
    usable_w = width - left - right
    usable_h = height - top - bottom
    points = []
    for i, val in enumerate(seq or [0]):
        x = left + (usable_w * i / (len(seq) - 1 if len(seq) > 1 else 1))
        y = top + usable_h * (1 - ((val - min_v) / span))
        points.append(f"{x:.0f},{y:.0f}")
    points_str = " ".join(points)

    # Métrica extra: producción por hectárea
    try:
        sup = float(p.superficie_ha or 0)
    except (TypeError, ValueError):
        sup = 0.0
    prod_por_ha = round((p.produccion_esperada_t or 0) / sup, 2) if sup > 0 else 0

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


# ======================
# API local: comunas por región (para el select dependiente)
# ======================

@require_GET
@login_required
def comunas_api(request, region_slug_value):
    """
    Devuelve {"region": "<nombre>", "comunas": [..]} según el slug de la región.
    Se usa desde el JS del formulario para poblar el select de comunas.
    """
    # Busca la región original a partir del slug (maneja tildes y apóstrofos)
    region_name = next(
        (r for r in COMUNAS_POR_REGION.keys() if region_slug(r) == region_slug_value),
        None,
    )
    comunas = COMUNAS_POR_REGION.get(region_name, [])
    return JsonResponse({"region": region_name, "comunas": comunas})

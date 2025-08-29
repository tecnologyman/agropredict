import json, math
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PrediccionForm
from .models import Prediccion

FRUIT_FACTOR = {'manzana':1.00, 'cereza':0.95}

def _baseline(superficie, temp_c, precip_mm, radiacion_wm2, arbol):
    base = 0.8 * superficie * FRUIT_FACTOR.get(arbol, 1.0)
    clima_score = (radiacion_wm2 / 1000.0) + (temp_c * 0.3) + (precip_mm * 0.002)
    produccion = max(0, base * (1 + (clima_score / 100)))
    proy = [round(produccion * (1 + i*0.05), 2) for i in range(5)]
    # recomendaciones simples
    recs = []
    if temp_c < 8: recs.append('Baja T°: riesgo de heladas, evaluar protecciones.')
    if precip_mm < 300: recs.append('Déficit hídrico: planificar riego suplementario.')
    if radiacion_wm2 > 1900: recs.append('Alta radiación: monitorear estrés hídrico.')
    if not recs: recs.append('Parámetros dentro de rangos medios para la zona.')
    return round(produccion,2), proy, recs

def _svg_points(values, width=800, height=240, left=50, right=20, top=20, bottom=20):
    if not values: values = [0]
    vmax = max(values); vmin = min(values)
    span = (vmax - vmin) or 1
    usable_w = width - left - right
    usable_h = height - top - bottom
    pts = []
    n = len(values)
    for i, v in enumerate(values):
        x = left + (usable_w * (0 if n == 1 else i/(n-1)))
        y = top + usable_h * (1 - ((v - vmin) / span))
        pts.append(f"{int(round(x))},{int(round(y))}")
    grid_x = [int(round(left + (usable_w * i / 5.0))) for i in range(1,5)]
    max_label = f"{math.ceil(vmax)}"
    return " ".join(pts), grid_x, max_label

@login_required
def dashboard(request):
    ultimas = list(Prediccion.objects.filter(usuario=request.user).order_by('-creado')[:5][::-1])
    valores = [p.produccion_esperada_t for p in ultimas] if ultimas else []
    dash_points, grid_x, max_label = _svg_points(valores, width=800, height=240, left=50, right=20, top=20, bottom=20)
    ctx = {
        'top_title':'Dashboard ejecutivo',
        'ultimas': ultimas,
        'dash_points': dash_points,
        'grid_x': grid_x,
        'max_label': max_label,
        # KPIs demo (offline)
        'kpi_riesgo_heladas':'Medio',
        'kpi_eto': 5.1,
        'kpi_ventana_riego':'Alta prob.',
        'kpi_pp7d':24,
    }
    return render(request, 'core/dashboard.html', ctx)

@login_required
def prediccion_form(request):
    if request.method == 'POST':
        form = PrediccionForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            prod, proy, _ = _baseline(d['superficie_ha'], d['temp_prom_anual_c'], d['precip_anual_mm'], d['radiacion_anual_wm2'], d['arbol_frutal'])
            p = Prediccion.objects.create(
                usuario=request.user,
                region=d['region'],
                arbol_frutal=d['arbol_frutal'],
                superficie_ha=d['superficie_ha'],
                temp_prom_anual_c=d['temp_prom_anual_c'],
                precip_anual_mm=d['precip_anual_mm'],
                radiacion_anual_wm2=d['radiacion_anual_wm2'],
                produccion_esperada_t=prod,
                proyeccion_json=json.dumps(proy),
            )
            return redirect('prediccion_resultado', pk=p.pk)
    else:
        form = PrediccionForm()
    return render(request, 'core/prediccion_form.html', {'form': form})

@login_required
def prediccion_resultado(request, pk):
    p = get_object_or_404(Prediccion, pk=pk, usuario=request.user)
    recomendaciones = []
    if request.method == 'POST':
        form = PrediccionForm(request.POST, instance=p)
        if form.is_valid():
            p = form.save(commit=False)
            prod, proy, recomendaciones = _baseline(p.superficie_ha, p.temp_prom_anual_c, p.precip_anual_mm, p.radiacion_anual_wm2, p.arbol_frutal)
            p.produccion_esperada_t = prod
            p.proyeccion_json = json.dumps(proy)
            p.save()
        else:
            recomendaciones = []
    else:
        form = PrediccionForm(instance=p)

    proy = json.loads(p.proyeccion_json) if p.proyeccion_json else []
    points, grid_x, max_label = _svg_points(proy, width=720, height=240, left=40, right=20, top=20, bottom=20)
    ctx = {
        'p': p,
        'form': form,
        'proy': proy,
        'points': points,
        'grid_x': grid_x,
        'max_label': max_label,
        'recomendaciones': recomendaciones,
    }
    return render(request, 'core/prediccion_resultado.html', ctx)

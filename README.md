# AgroPredict · MVP Django (Sprint 1)

Proyecto monolítico Django listo para correr **offline** (SQLite), con:

- Login/Logout usando `django.contrib.auth` (`/accounts/login/`)
- Dashboard básico (`/`) con últimas 5 predicciones del usuario
- Formulario de **Predicción** (`/prediccion/`) y página de **Resultado** (`/prediccion/<id>/`)
- Cálculo baseline explicable y gráfico **SVG inline** (sin librerías externas)
- Estilos CSS minimalista en español y sin dependencias externas

## Requisitos
- Python 3.10+
- (Opcional) `venv` para entorno virtual

## Instalación (paso a paso)
1. Crear y activar entorno:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Migraciones y superusuario:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
4. Ejecutar servidor:
   ```bash
   python manage.py runserver
   ```
5. Abrir en el navegador:
   - Login: http://127.0.0.1:8000/accounts/login/
   - App: http://127.0.0.1:8000/

## Cálculo baseline (para demo)
```text
base = 0.8 * superficie_ha
clima_score = (radiacion_anual_wm2 / 1000.0) + (temp_prom_anual_c * 0.3) + (precip_anual_mm * 0.002)
produccion_esperada_t = max(0, base * (1 + (clima_score / 100)))
proyeccion (5 periodos) = produccion * (1 + i*0.05) con i=0..4 (redondeado a 2 decimales)
```

La proyección se representa como una polilínea SVG **inline** para funcionar sin internet.

## Cómo probar la demo (ejemplo)
- **Datos**: Región *Maule*; Superficie **10** ha; Temp. **15 °C**; Precip. **800 mm**; Radiación **1800 W/m²**.
- **Cálculo**:
  - base = 0.8 × 10 = 8.0
  - clima_score = 1800/1000 + 15×0.3 + 800×0.002 = 1.8 + 4.5 + 1.6 = **7.9**
  - producción ≈ 8.0 × (1 + 7.9/100) = 8.0 × 1.079 = **8.63 t** (aprox.)
  - proyección 5 periodos: [8.63, 9.06, 9.49, 9.92, 10.35] (aprox.)
- **Qué verás**: página de resultado con **resumen**, tarjeta **“Producción esperada (t)”**, **tabla** y **gráfico SVG** con 5 puntos.

## Estructura relevante
```
agropredict_project/
├─ core/
│  ├─ admin.py
│  ├─ forms.py
│  ├─ models.py
│  └─ views.py
├─ templates/
│  ├─ base.html
│  ├─ registration/login.html
│  └─ core/...
├─ static/css/styles.css
├─ manage.py
├─ agropredict_project/
│  ├─ __init__.py
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
└─ requirements.txt
```

## Reemplazar baseline por modelo/servicio real (Sprints futuros)
Sustituir la función `_baseline(...)` y su uso en `core/views.py` dentro de `prediccion_form` por una llamada a su servicio local o del framework de Neering. Ejemplo (pseudo-código):

```python
# core/views.py
def _baseline(...):
    # TODO: reemplazar por cliente del modelo real
    # from neering_sdk import ClienteModelo
    # cliente = ClienteModelo(ruta_modelo_local)
    # return cliente.predecir(superficie, temp_c, precip_mm, radiacion_wm2)
    ...
```

## Admin (opcional)
- Panel en `/admin/` para explorar predicciones
- `PrediccionAdmin` con `list_display` y filtros

---

**Nota:** Todo el texto y UI están en español (Chile) y el sitio funciona **offline** (sin dependencias externas).

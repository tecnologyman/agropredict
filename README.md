# AgroPredict · MVP Django (Sprint 1, estilo Treering)

Proyecto monolítico Django listo para correr **offline** (SQLite), con:

- Login/Logout (`/accounts/login/`, `/accounts/logout/`)
- Dashboard con KPIs demo y gráfico SVG de las **últimas 5 producciones**
- **Predicción** con formulario (incluye **Árbol frutal: Manzana/Cereza**)
- **Detalle editable**: puedes modificar parámetros y recalcular; incluye cambio rápido de frutal
- Gráficos **SVG inline** (sin dependencias externas)
- Estilo visual: sidebar morado→magenta, topbar con usuario y botón **Salir**, pie “Hecho por Treering · Demo offline Sprint 1”

## Requisitos
- Python 3.10+
- (Opcional) `venv`

## Instalación
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Rutas
- Login: http://127.0.0.1:8000/accounts/login/
- Dashboard: http://127.0.0.1:8000/
- Predicción (nueva): http://127.0.0.1:8000/prediccion/
- Resultado/edición: http://127.0.0.1:8000/prediccion/<id>/

## Cálculo baseline (demo)
```
base = 0.8 * superficie_ha * factor_frutal   # manzana=1.00, cereza=0.95
clima_score = (radiacion/1000) + (temp*0.3) + (precip*0.002)
produccion_esperada_t = max(0, base * (1 + clima_score/100))
proyeccion 5T = produccion * (1 + i*0.05)  para i=0..4
```

## Probar con ejemplo
- Frutal: Manzana
- Región: Maule
- Superficie: 10 ha
- Temp: 15 °C
- Precip: 800 mm
- Radiación: 1800 W/m²

Esperado: **~8.63 t**, proyección **[8.63, 9.06, 9.49, 9.92, 10.35]**.

## Reemplazar baseline por modelo real
Editar `core/views.py` → `_baseline(...)` para invocar su servicio o framework Neering y guardar:
- `produccion_esperada_t` (float)
- `proyeccion_json` (lista de 5 valores en JSON)

---
© AgroPredict · Hecho por Treering · **MVP demo offline (Sprint 1)**

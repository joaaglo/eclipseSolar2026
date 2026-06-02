# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Contexto

Herramienta de planificación para el eclipse solar total del **12 de agosto de 2026**, observable desde España. Origen fijo: **Alboraya (46120, Valencia)** — coordenadas `39.5516, -0.3373`.

La totalidad ocurre al atardecer (~20:26–20:33h hora local), con el Sol muy bajo en el horizonte oeste. Prioridad: sitios con horizonte despejado al oeste y mayor duración de totalidad.

## Ejecutar

```bash
python eclipse.py all           # rutas OSRM + distancia a centerline → CSV
python eclipse.py all --xlsx    # ídem + genera Excel
python eclipse.py routes        # solo rutas OSRM
python eclipse.py centerline    # solo distancia a línea central
```

Requiere Python 3 y conexión a internet. `all` hace ~190 llamadas HTTP a `router.project-osrm.org` con 300 ms de pausa (~1 minuto total).

Dependencias opcionales (solo para `--xlsx`):
```bash
pip install openpyxl pandas
```

## Arquitectura

Un único script **`eclipse.py`** con funciones `cmd_routes()`, `cmd_centerline()`, `cmd_xlsx()` y CLI via argparse. Lee los sitios de **`sites.json`** (190 entradas con espacio, municipio, tipo, capacidad, parking, inicio_totalidad, duracion_totalidad, lat, lng).

- **`sites.json`** — datos fuente de los 190 sitios oficiales (El País / widget junio 2026, basado en IGN/OAN). Duración de totalidad calculada por el IGN para las coordenadas exactas de cada sitio.
- **`eclipse_sitios.csv`** — copia de referencia original, no se usa en el proceso.
- **`output/eclipse_sitios_rutas.csv`** — output generado con columnas: Espacio, Municipio, Tipo, Capacidad, Parking, Inicio totalidad, Duración totalidad, Lat, Lng, Dist_carretera_km, Tiempo_Maps, Dist_centerline_km.
- **`output/eclipse_sitios_rutas.xlsx`** — ídem con formato Excel (filtros, cabecera azul, freeze pane).

## Notas clave

- La duración máxima de totalidad en línea central es ~1m 50s (Asturias/Galicia). Los sitios más cercanos con totalidad útil son Malvarrosa (1m 00s) y Puzol (1m 13s); Peñíscola y Benasal ofrecen ~1m 39s a ~2–3h en coche.
- `Tiempo_Maps` tiene formato `00h 00min` (padding de dos cifras en ambos campos) para que ordene correctamente como texto.
- `Duración totalidad` tiene formato `0m 00s` (sin padding en minutos, dos cifras en segundos) por el mismo motivo.
- `Dist_centerline_km` usa cross-track distance esférica al segmento más cercano de la polilínea NASA.
- OSRM es gratuito y sin API key — mantener la pausa de 300 ms.
- La línea central NASA está hardcodeada en `eclipse.py` como lista `CENTERLINE` (~46 puntos cada 2 minutos de tiempo).

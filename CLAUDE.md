# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Contexto

Herramienta de planificación para el eclipse solar total del **12 de agosto de 2026**, observable desde España. Origen fijo: **Alboraya (46120, Valencia)** — coordenadas `39.5516, -0.3373`.

La totalidad ocurre al atardecer (~20:26–20:33h hora local), con el Sol muy bajo en el horizonte oeste. Prioridad: sitios con horizonte despejado al oeste y mayor duración de totalidad.

## Ejecutar

```bash
python get_routes.py
```

Requiere Python 3 y conexión a internet. Genera `eclipse_sitios_rutas.csv` con distancias y tiempos en coche desde Alboraya para los 190 sitios. Hace ~190 llamadas HTTP a `router.project-osrm.org` con 300 ms de pausa entre ellas (~1 minuto total).

## Arquitectura

- **`get_routes.py`** — script único. La lista `SITES` (190 entradas) está hardcodeada como tuplas `(nombre, municipio, tipo, capacidad, parking, inicio_totalidad, duración_totalidad, lat, lng)`. La función `get_route()` llama a OSRM y devuelve `(dist_km, dur_str)`. `main()` itera, imprime progreso y escribe el CSV de salida.
- **`eclipse_sitios.csv`** — datos fuente de los 190 sitios oficiales (El País / trioeclipses.es), sin columnas de ruta.
- **`eclipse_sitios_rutas.csv`** — output generado, añade `Dist_carretera_km` y `Tiempo_Maps`.

## Notas clave

- La duración máxima de totalidad en línea central es ~1m 50s (Asturias/Galicia). Los sitios más cercanos con totalidad útil son Malvarrosa (1m 00s) y Puzol (1m 13s); Peñíscola y Benasal ofrecen ~1m 39s a ~2–3h en coche.
- OSRM es gratuito y sin API key, pero es un servicio público — mantener la pausa de 300 ms.

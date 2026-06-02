# Eclipse Solar Total — 12 agosto 2026

Planificación de observación para Joan y Sabine desde **Alboraya (46120, Valencia)**.

## Contexto

El 12 de agosto de 2026 tendrá lugar el primer eclipse total de Sol visible desde la península ibérica en más de un siglo. La totalidad ocurre al **atardecer** (entorno a las 20:26–20:33 hora local según ubicación), con el Sol muy bajo en el horizonte oeste.

La franja de totalidad atraviesa de oeste a este: Galicia → Asturias → Cantabria → Castilla y León → La Rioja → Navarra → Aragón → Castellón/Valencia (norte) → Cataluña (sur).

## Fuente de datos

Lista oficial de **190 sitios de observación** extraída del widget de El País (junio 2026), basada en los datos de la Comisión Interministerial Trío de Eclipses (trioeclipses.es).

## Archivos

| Archivo | Descripción |
|---|---|
| `eclipse_sitios.csv` | 190 sitios con tipo, capacidad, parking, hora de inicio y duración de totalidad. Distancia por carretera y tiempo pendientes (ver abajo). |
| `get_routes.py` | Script Python que consulta OSRM (OpenStreetMap, sin API key) para calcular distancia real por carretera y tiempo estimado en coche desde Alboraya para los 190 sitios. Genera `eclipse_sitios_rutas.csv`. |

## Uso

```bash
cd eclipseSolar
python get_routes.py
```

Requiere Python 3 y conexión a internet. Hace ~190 llamadas a `router.project-osrm.org` con 300ms de pausa. Tiempo estimado: ~1 minuto. Output: `eclipse_sitios_rutas.csv`.

## Sitios más cercanos a Alboraya con totalidad

| Sitio | Municipio | Duración totalidad |
|---|---|---|
| Playa de la Malvarrosa | Valencia | 1m 00s |
| Playa de Puzol | Puzol (Valencia) | 1m 13s |
| Playas del Pinar y del Gurugú | Castellón de la Plana | 1m 33s |
| Ermita de San Cristóbal | Benasal (Castellón) | 1m 39s |
| Parque municipal de Les Useres | Les Useres (Castellón) | 1m 37s |
| Peñíscola | Peñíscola (Castellón) | 1m 39s |
| Plaça de bous de Alcanar | Alcanar (Tarragona) | 1m 37s |

## Notas

- La duración máxima de totalidad en línea central es ~1m 50s (Asturias/Galicia).
- Al estar en Valencia, el Sol estará **muy bajo** en el horizonte oeste durante la totalidad — priorizar sitios con horizonte despejado al oeste.
- Malvarrosa y Puzol son los únicos sitios oficiales dentro de la provincia de Valencia con eclipse total.

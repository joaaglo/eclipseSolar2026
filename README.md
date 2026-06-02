# Eclipse Solar Total — 12 agosto 2026

Planificación de observación para Joan y Sabine desde **Alboraya (46120, Valencia)**.

## Contexto

El 12 de agosto de 2026 tendrá lugar el primer eclipse total de Sol visible desde la península ibérica en más de un siglo. La totalidad ocurre al **atardecer** (entorno a las 20:26–20:33 hora local según ubicación), con el Sol muy bajo en el horizonte oeste.

La franja de totalidad atraviesa de oeste a este: Galicia → Asturias → Cantabria → Castilla y León → La Rioja → Navarra → Aragón → Castellón/Valencia (norte) → Cataluña (sur).

## Fuente de datos

Lista oficial de **190 sitios de observación** extraída del widget de El País (junio 2026), basada en los datos de la Comisión Interministerial Trío de Eclipses (trioeclipses.es) y el IGN. La duración de totalidad es específica para las coordenadas de cada sitio.

## Archivos

| Archivo | Descripción |
|---|---|
| `sites.json` | 190 sitios con coordenadas, tipo, capacidad, parking, hora de inicio y duración de totalidad. |
| `eclipse.py` | Script principal con CLI. Calcula rutas OSRM y distancia a la línea central. |
| `eclipse_sitios.csv` | Copia de referencia original. No se usa en el proceso. |
| `output/eclipse_sitios_rutas.csv` | Output generado con todas las columnas. |
| `output/eclipse_sitios_rutas.xlsx` | Ídem en Excel con filtros y formato. |

## Uso

```bash
python eclipse.py all           # rutas OSRM + distancia a centerline
python eclipse.py all --xlsx    # ídem + genera Excel
python eclipse.py --help        # ayuda
```

Requiere Python 3 y conexión a internet (~1 minuto para las 190 rutas).
Para el Excel: `pip install openpyxl pandas`.

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

# La Vueltita · Eclipse Solar 2026

Planificador interactivo para el eclipse solar total del **12 de agosto de 2026** observable desde España.

## Qué hace

- Muestra la banda de totalidad del eclipse sobre un mapa interactivo (datos NASA)
- Marca los 190 sitios oficiales de observación (fuente: El País / IGN), coloreados por duración de totalidad
- Calcula desde tu posición (GPS o clic en el mapa) cuáles son los mejores sitios accesibles en el tiempo que elijas
- Comparte el resultado por WhatsApp o Twitter

## Stack

React + Vite · react-leaflet · OpenStreetMap · OSRM (routing)

## Desarrollo local

```bash
npm install
npm run dev
```

## Datos

- Sitios de observación: `public/elpais_eclipse2026_sitiosOficiales.json` (190 entradas, fuente El País / IGN)
- Banda de totalidad: `src/data/eclipseBand.js` (coordenadas NASA GSFC)
- Rutas: OSRM public demo server (no comercial, sin API key)

## Aviso

Los tiempos de desplazamiento son orientativos (OSRM, tráfico estándar). No reflejan las condiciones reales el día del eclipse ni la disponibilidad de plazas en cada sitio.

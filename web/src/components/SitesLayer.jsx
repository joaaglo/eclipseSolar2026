import { CircleMarker, Popup } from 'react-leaflet'
import { durationColor } from '../utils/ranking'

export default function SitesLayer({ sites, results }) {
  const resultIds = new Set(results?.top?.map(s => s.espacio) ?? [])
  const bonusIds = new Set(results?.bonus?.map(s => s.espacio) ?? [])

  return sites.map(site => {
    const isResult = resultIds.has(site.espacio)
    const isBonus = bonusIds.has(site.espacio)
    const color = durationColor(site.duracion_totalidad)
    const radius = isResult ? 10 : isBonus ? 8 : 6
    const weight = isResult || isBonus ? 2.5 : 1

    return (
      <CircleMarker
        key={site.espacio}
        center={[site.lat, site.lng]}
        radius={radius}
        pathOptions={{
          color: isResult ? '#fff' : isBonus ? '#ffe082' : '#333',
          fillColor: color,
          fillOpacity: isResult ? 1 : isBonus ? 0.95 : 0.75,
          weight,
        }}
      >
        <Popup>
          <div style={{ minWidth: 180 }}>
            <strong>{site.espacio}</strong>
            <br />
            <span style={{ color: '#666' }}>{site.municipio}</span>
            <br />
            <br />
            <span>⏱ Totalidad: <strong>{site.duracion_totalidad}</strong></span>
            <br />
            <span>🕐 Inicio: {site.inicio_totalidad}</span>
            <br />
            <span>🅿️ Parking: {site.parking}</span>
            {site.travelSecs != null && (
              <>
                <br />
                <span>🚗 Tiempo: <strong>{formatTravel(site.travelSecs)}</strong></span>
              </>
            )}
          </div>
        </Popup>
      </CircleMarker>
    )
  })
}

function formatTravel(secs) {
  const h = Math.floor(secs / 3600)
  const m = Math.floor((secs % 3600) / 60)
  if (h === 0) return `${m} min`
  if (m === 0) return `${h}h`
  return `${h}h ${m}min`
}

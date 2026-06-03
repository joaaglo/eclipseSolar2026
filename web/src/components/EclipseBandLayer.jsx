import { Polygon, Polyline, Marker } from 'react-leaflet'
import { divIcon } from 'leaflet'
import { BAND_POLYGON, CENTERLINE_SMOOTH, EAST_CAP_SOUTH } from '../data/eclipseBand'

const ptIcon = (label, color) => divIcon({
  html: `<div style="font-size:11px;font-weight:900;color:${color};line-height:1;white-space:nowrap">✕ ${label}</div>`,
  iconAnchor: [8, 8],
  className: '',
})

export default function EclipseBandLayer() {
  return (
    <>
      <Polygon
        positions={BAND_POLYGON}
        pathOptions={{
          color: '#4A6FA5',
          fillColor: '#4A6FA5',
          fillOpacity: 0.18,
          weight: 1,
          opacity: 0.5,
        }}
      />
      <Polyline
        positions={CENTERLINE_SMOOTH}
        pathOptions={{
          color: '#1a3a6b',
          weight: 1.5,
          opacity: 0.7,
          dashArray: '6 4',
        }}
      />
      {/* DEBUG — S★ */}
      <Marker position={EAST_CAP_SOUTH} icon={ptIcon('S★', '#00a040')} />
    </>
  )
}

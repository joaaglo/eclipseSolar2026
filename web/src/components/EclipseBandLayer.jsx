import { Polygon, Polyline } from 'react-leaflet'
import { BAND_POLYGON, CENTERLINE } from '../data/eclipseBand'

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
        positions={CENTERLINE}
        pathOptions={{
          color: '#1a3a6b',
          weight: 1.5,
          opacity: 0.7,
          dashArray: '6 4',
        }}
      />
    </>
  )
}

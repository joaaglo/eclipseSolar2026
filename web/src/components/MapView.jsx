import { useEffect } from 'react'
import { MapContainer, TileLayer, useMapEvents, useMap, CircleMarker } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import EclipseBandLayer from './EclipseBandLayer'
import SitesLayer from './SitesLayer'

function ClickHandler({ onMapClick }) {
  useMapEvents({ click: e => onMapClick({ lat: e.latlng.lat, lng: e.latlng.lng }) })
  return null
}

function FlyToSite({ focusSite }) {
  const map = useMap()
  useEffect(() => {
    if (!focusSite) return
    const zoom = Math.max(map.getZoom(), 11)
    map.flyTo([focusSite.site.lat, focusSite.site.lng], zoom, { duration: 1.2 })
  }, [focusSite])
  return null
}

export default function MapView({ origin, onMapClick, showBand, showSites, sites, results, focusSite }) {
  return (
    <MapContainer
      center={[43, -5]}
      zoom={5}
      className="map"
      zoomControl={true}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />

      {showBand && <EclipseBandLayer />}
      {showSites && sites.length > 0 && (
        <SitesLayer sites={sites} results={results} focusSite={focusSite?.site} />
      )}

      {origin && (
        <CircleMarker
          center={[origin.lat, origin.lng]}
          radius={10}
          pathOptions={{
            color: '#fff',
            fillColor: '#2563eb',
            fillOpacity: 1,
            weight: 2.5,
          }}
        />
      )}

      <ClickHandler onMapClick={onMapClick} />
      <FlyToSite focusSite={focusSite} />
    </MapContainer>
  )
}

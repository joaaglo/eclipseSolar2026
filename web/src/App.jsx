import { useState, useEffect } from 'react'
import MapView from './components/MapView'
import SearchPanel from './components/SearchPanel'
import { useUserLocation } from './hooks/useUserLocation'
import { fetchRoutes } from './utils/osrm'
import { getBestSites } from './utils/ranking'

export default function App() {
  const [sites, setSites] = useState([])
  const [origin, setOrigin] = useState(null)
  const [maxMinutes, setMaxMinutes] = useState(120)
  const [showBand, setShowBand] = useState(true)
  const [showSites, setShowSites] = useState(true)
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [focusSite, setFocusSite] = useState(null)
  const handleSiteClick = site => setFocusSite({ site, t: Date.now() })

  const { location: geoLocation, loading: geoLoading, error: geoError, request: requestGeo } = useUserLocation()

  useEffect(() => {
    fetch('/elpais_eclipse2026_sitiosOficiales.json')
      .then(r => r.json())
      .then(setSites)
      .catch(() => setError('No se pudieron cargar los sitios'))
  }, [])

  useEffect(() => {
    if (geoLocation && !origin) setOrigin(geoLocation)
  }, [geoLocation])

  useEffect(() => {
    const p = new URLSearchParams(window.location.search)
    const lat = parseFloat(p.get('lat'))
    const lng = parseFloat(p.get('lng'))
    const maxmin = parseInt(p.get('maxmin'))
    if (!isNaN(lat) && !isNaN(lng)) {
      setOrigin({ lat, lng })
      if (!isNaN(maxmin)) setMaxMinutes(maxmin)
    }
  }, [])

  const handleCalculate = async () => {
    if (!origin || sites.length === 0) return
    setLoading(true)
    setError(null)
    setResults(null)
    try {
      const { durations } = await fetchRoutes(origin, sites)
      const best = getBestSites(durations, null, sites, maxMinutes)
      setResults(best)
    } catch (e) {
      setError(`Error al calcular rutas: ${e.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="layout">
      <SearchPanel
        origin={origin} setOrigin={setOrigin}
        maxMinutes={maxMinutes} setMaxMinutes={setMaxMinutes}
        showBand={showBand} setShowBand={setShowBand}
        showSites={showSites} setShowSites={setShowSites}
        results={results}
        loading={loading}
        error={error}
        onCalculate={handleCalculate}
        onSiteClick={handleSiteClick}
        geoLoading={geoLoading}
        geoError={geoError}
        requestGeo={requestGeo}
      />
      <MapView
        origin={origin}
        onMapClick={setOrigin}
        showBand={showBand}
        showSites={showSites}
        sites={sites}
        results={results}
        focusSite={focusSite}
      />
    </div>
  )
}

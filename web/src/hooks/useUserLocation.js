import { useState, useEffect } from 'react'

export function useUserLocation() {
  const [location, setLocation] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const request = () => {
    if (!navigator.geolocation) {
      setError('Tu navegador no soporta geolocalización')
      return
    }
    setLoading(true)
    setError(null)
    navigator.geolocation.getCurrentPosition(
      pos => {
        setLocation({ lat: pos.coords.latitude, lng: pos.coords.longitude })
        setLoading(false)
      },
      err => {
        setError('No se pudo obtener tu ubicación')
        setLoading(false)
      },
      { timeout: 10000 }
    )
  }

  useEffect(() => { request() }, [])

  return { location, error, loading, request }
}

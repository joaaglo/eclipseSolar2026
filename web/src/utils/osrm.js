const OSRM_BASE = 'https://router.project-osrm.org/table/v1/driving'

export async function fetchRoutes(origin, sites) {
  const coords = [
    `${origin.lng},${origin.lat}`,
    ...sites.map(s => `${s.lng},${s.lat}`),
  ].join(';')

  const destIndices = sites.map((_, i) => i + 1).join(',')
  const url = `${OSRM_BASE}/${coords}?sources=0&destinations=${destIndices}&annotations=duration,distance`

  const res = await fetch(url)
  if (!res.ok) throw new Error(`OSRM error ${res.status}`)
  const data = await res.json()
  if (data.code !== 'Ok') throw new Error(`OSRM: ${data.code}`)

  return {
    durations: data.durations[0],
    distances: data.distances?.[0] ?? null,
  }
}

const OSRM_BASE = 'https://router.project-osrm.org/table/v1/driving'
// Public OSRM demo server limit: 100 elements (sources + destinations)
const BATCH_SIZE = 99

export async function fetchRoutes(origin, sites) {
  const batches = []
  for (let i = 0; i < sites.length; i += BATCH_SIZE) {
    batches.push(sites.slice(i, i + BATCH_SIZE))
  }

  const results = await Promise.all(batches.map(batch => fetchBatch(origin, batch)))

  return {
    durations: results.flatMap(r => r.durations),
    distances: results.flatMap(r => r.distances),
  }
}

async function fetchBatch(origin, batch) {
  const coords = [
    `${origin.lng},${origin.lat}`,
    ...batch.map(s => `${s.lng},${s.lat}`),
  ].join(';')

  const destIndices = batch.map((_, i) => i + 1).join(',')
  const url = `${OSRM_BASE}/${coords}?sources=0&destinations=${destIndices}&annotations=duration,distance`

  const res = await fetch(url)
  if (!res.ok) throw new Error(`OSRM error ${res.status}`)
  const data = await res.json()
  if (data.code !== 'Ok') throw new Error(`OSRM: ${data.code}`)

  const durations = data.durations[0].slice(1)
  const distances = data.distances?.[0].slice(1) ?? batch.map(() => null)
  return { durations, distances }
}

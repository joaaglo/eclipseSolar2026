const OSRM_BASE = 'https://router.project-osrm.org/table/v1/driving'
// Safe batch size: 1 origin + 50 destinations = 51 coords, well under any server limit
const BATCH_SIZE = 50

export async function fetchRoutes(origin, sites) {
  const batches = []
  for (let i = 0; i < sites.length; i += BATCH_SIZE) {
    batches.push(sites.slice(i, i + BATCH_SIZE))
  }

  const results = await Promise.all(batches.map(batch => fetchBatch(origin, batch)))

  return {
    durations: results.flatMap(r => r.durations),
  }
}

async function fetchBatch(origin, batch) {
  const coords = [
    `${origin.lng},${origin.lat}`,
    ...batch.map(s => `${s.lng},${s.lat}`),
  ].join(';')

  // OSRM Table API uses semicolons as separators for sources/destinations indices
  const destIndices = batch.map((_, i) => i + 1).join(';')
  const url = `${OSRM_BASE}/${coords}?sources=0&destinations=${destIndices}&annotations=duration`

  const res = await fetch(url)
  if (!res.ok) {
    const body = await res.text().catch(() => '')
    throw new Error(`OSRM error ${res.status}: ${body}`)
  }
  const data = await res.json()
  if (data.code !== 'Ok') throw new Error(`OSRM: ${data.code}`)

  // durations[0] has exactly N entries (one per destination) — no slice needed
  return { durations: data.durations[0] }
}

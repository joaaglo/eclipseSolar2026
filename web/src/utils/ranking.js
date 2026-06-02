export function parseDuration(str) {
  if (!str) return 0
  const m = str.match(/(\d+)m\s*(\d+)s/)
  if (!m) return 0
  return parseInt(m[1]) * 60 + parseInt(m[2])
}

export function durationColor(durationStr) {
  const secs = parseDuration(durationStr)
  const minS = 30, maxS = 110
  const t = Math.max(0, Math.min(1, (secs - minS) / (maxS - minS)))
  const r = Math.round(255 + (180 - 255) * t)
  const g = Math.round(200 + (20 - 200) * t)
  const b = Math.round(0 + (20 - 0) * t)
  return `rgb(${r},${g},${b})`
}

export function getBestSites(durations, distances, sites, maxMinutes) {
  const maxSecs = maxMinutes * 60
  const bonusBuffer = 10 * 60

  const withTravel = sites.map((site, i) => ({
    ...site,
    travelSecs: durations[i] ?? null,
  })).filter(s => s.travelSecs !== null)

  const sorter = (a, b) => parseDuration(b.duracion_totalidad) - parseDuration(a.duracion_totalidad)

  const top = withTravel
    .filter(s => s.travelSecs <= maxSecs)
    .sort(sorter)
    .slice(0, 10)

  const bonus = withTravel
    .filter(s => s.travelSecs > maxSecs && s.travelSecs <= maxSecs + bonusBuffer)
    .sort(sorter)
    .slice(0, 3)

  return { top, bonus }
}

export function formatTravel(secs) {
  const h = Math.floor(secs / 3600)
  const m = Math.floor((secs % 3600) / 60)
  if (h === 0) return `${m} min`
  if (m === 0) return `${h}h`
  return `${h}h ${m}min`
}

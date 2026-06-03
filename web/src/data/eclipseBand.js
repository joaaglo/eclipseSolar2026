// Eclipse path data for 2026 Aug 12. Source: NASA GSFC
// https://eclipse.gsfc.nasa.gov/SEpath/SEpath2001/SE2026Aug12Tpath.html
// Coordinates: [lat, lng] decimal degrees, 2-minute intervals

export const CENTERLINE = [
  [82.275, 112.487], [85.295, 104.215], [87.278, 81.525],
  [87.823, 33.000],  [86.835, -1.638],  [85.403, -15.182],
  [83.932, -21.187], [82.495, -24.272], [81.110, -25.992],
  [79.773, -26.982], [78.483, -27.540], [77.233, -27.825],
  [76.017, -27.928], [74.837, -27.905], [73.683, -27.788],
  [72.557, -27.603], [71.450, -27.362], [70.365, -27.078],
  [69.298, -26.760], [68.247, -26.410], [67.210, -26.032],
  [66.185, -25.630], [65.172, -25.205], [64.168, -24.757],
  [63.172, -24.287], [62.183, -23.793], [61.200, -23.277],
  [60.222, -22.737], [59.245, -22.170], [58.272, -21.573],
  [57.297, -20.947], [56.322, -20.287], [55.343, -19.588],
  [54.362, -18.847], [53.372, -18.057], [52.372, -17.212],
  [51.360, -16.303], [50.333, -15.317], [49.285, -14.238],
  [48.212, -13.048], [47.102, -11.715], [45.943, -10.190],
  [44.713, -8.398],  [43.372, -6.188],  [41.817, -3.185],
  [39.408, 2.950],
]

export const NORTH_LIMIT = [
  [75.9367, 108.7583], [82.1633, 103.2167], [84.85, 90.395],
  [86.3433, 65.8233],  [86.545, 32.7283],   [85.72, 8.375],
  [84.4817, -4.81],    [83.1317, -12.0017], [81.775, -16.2167],
  [80.4417, -18.8417], [79.1417, -20.5383], [77.875, -21.6567],
  [76.6417, -22.3933], [75.44, -22.865],    [74.2667, -23.145],
  [73.1167, -23.285],  [71.9917, -23.3133], [70.885, -23.2583],
  [69.7983, -23.1317], [68.7267, -22.9483], [67.67, -22.7133],
  [66.6267, -22.4367], [65.5933, -22.12],   [64.5717, -21.7683],
  [63.5567, -21.3817], [62.5483, -20.9617], [61.5467, -20.5083],
  [60.5483, -20.0217], [59.5533, -19.5],    [58.56, -18.9433],
  [57.565, -18.3483],  [56.5683, -17.7117], [55.5683, -17.0283],
  [54.5617, -16.295],  [53.5467, -15.5033], [52.52, -14.6467],
  [51.4783, -13.7117], [50.4167, -12.685],  [49.33, -11.5467],
  [48.2083, -10.2667], [47.0383, -8.8017],  [45.8017, -7.0767],
  [44.4567, -4.9483],  [42.9083, -2.085],   [40.665, 3.295],
]

export const SOUTH_LIMIT = [
  [85.3217, 119.4233], [87.7533, 108.4317], [89.0667, 38.1483],
  [87.7883, -19.5067], [86.1417, -29.2167], [84.565, -32.2467],
  [83.0717, -33.4167], [81.65, -33.8383],   [80.2917, -33.8967],
  [78.9867, -33.76],   [77.7267, -33.505],  [76.5067, -33.1783],
  [75.3233, -32.805],  [74.1683, -32.4],    [73.0433, -31.9717],
  [71.94, -31.5267],   [70.86, -31.0683],   [69.7967, -30.6],
  [68.7533, -30.12],   [67.7233, -29.6317], [66.7067, -29.1333],
  [65.7033, -28.625],  [64.71, -28.1067],   [63.7267, -27.5767],
  [62.75, -27.0333],   [61.78, -26.4767],   [60.8167, -25.905],
  [59.8567, -25.3167], [58.9, -24.7067],    [57.945, -24.0767],
  [56.99, -23.4217],   [56.0367, -22.7383], [55.0783, -22.025],
  [54.1183, -21.275],  [53.1517, -20.485],  [52.1767, -19.6467],
  [51.1933, -18.755],  [50.195, -17.7983],  [49.1817, -16.765],
  [48.1467, -15.6383], [47.0833, -14.3967], [45.9833, -13.0083],
  [44.8317, -11.42],   [43.6067, -9.5517],  [42.2633, -7.2367],
  [40.6833, -4.04],
]

// Catmull-Rom spline: genera puntos interpolados suaves entre los puntos de control.
// Pasa exactamente por todos los puntos de control. n = puntos por segmento.
function catmullRom(pts, n = 10) {
  if (pts.length < 2) return pts
  const result = []
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[Math.max(0, i - 1)]
    const p1 = pts[i]
    const p2 = pts[i + 1]
    const p3 = pts[Math.min(pts.length - 1, i + 2)]
    for (let j = 0; j < n; j++) {
      const t = j / n
      const t2 = t * t
      const t3 = t2 * t
      const lat = 0.5 * (
        2 * p1[0] +
        (-p0[0] + p2[0]) * t +
        (2*p0[0] - 5*p1[0] + 4*p2[0] - p3[0]) * t2 +
        (-p0[0] + 3*p1[0] - 3*p2[0] + p3[0]) * t3
      )
      const lng = 0.5 * (
        2 * p1[1] +
        (-p0[1] + p2[1]) * t +
        (2*p0[1] - 5*p1[1] + 4*p2[1] - p3[1]) * t2 +
        (-p0[1] + 3*p1[1] - 3*p2[1] + p3[1]) * t3
      )
      result.push([lat, lng])
    }
  }
  result.push(pts[pts.length - 1])
  return result
}

const clip64 = pts => pts.filter(([lat]) => lat <= 64)

// Cap oeste: lat exacta de S26 (44.8317°N) — punto natural donde el cap queda horizontal
const CAP_WEST_LAT = 44.8317
const clipCap = pts => pts.filter(([lat]) => lat <= CAP_WEST_LAT)

// ---------------------------------------------------------------------------
// Cap este: S★ via recta slope-0.7 desde N21 × curva S extrapolada (sin S23)
// S23 se incluye como punto de control intermedio en la curva sur.
// ---------------------------------------------------------------------------

function polyFitLng(points) {
  let s0=0,s1=0,s2=0,s3=0,s4=0,r0=0,r1=0,r2=0
  for (const [lat,lng] of points) {
    s0++; s1+=lat; s2+=lat*lat; s3+=lat*lat*lat; s4+=lat*lat*lat*lat
    r0+=lng; r1+=lat*lng; r2+=lat*lat*lng
  }
  const M=[[s0,s1,s2,r0],[s1,s2,s3,r1],[s2,s3,s4,r2]]
  for (let col=0;col<3;col++) {
    let piv=col
    for (let r=col+1;r<3;r++) if (Math.abs(M[r][col])>Math.abs(M[piv][col])) piv=r
    ;[M[col],M[piv]]=[M[piv],M[col]]
    for (let r=col+1;r<3;r++) {
      const f=M[r][col]/M[col][col]
      for (let j=col;j<=3;j++) M[r][j]-=f*M[col][j]
    }
  }
  const x=[0,0,0]
  for (let i=2;i>=0;i--) {
    x[i]=M[i][3]
    for (let j=i+1;j<3;j++) x[i]-=M[i][j]*x[j]
    x[i]/=M[i][i]
  }
  return lat => x[0]+x[1]*lat+x[2]*lat*lat
}

function intersect07(lngS) {
  const N21     = NORTH_LIMIT[NORTH_LIMIT.length - 1]
  const lngLine = lat => N21[1] + 0.7 * (lat - N21[0])
  let prevLat = 43, prevDiff = lngLine(43) - lngS(43)
  for (let lat = 42.9; lat > 34; lat -= 0.05) {
    const diff = lngLine(lat) - lngS(lat)
    if (prevDiff * diff < 0) {
      const latInt = prevLat + (prevDiff / (prevDiff - diff)) * (lat - prevLat)
      return [latInt, lngS(latInt)]
    }
    prevLat = lat; prevDiff = diff
  }
  return null
}

// S1…S22 (sin S23)
const S_VALID = clip64(SOUTH_LIMIT).slice(0, -1)
const S22     = S_VALID[S_VALID.length - 1]   // [42.2633, -7.2367]

// 6 candidatos P3..P8 — fit cuadrático con los últimos N puntos de S1…S22
export const EAST_CAP_CANDIDATES = [3, 4, 5, 6, 7, 8].map(nPts => {
  const lngS  = polyFitLng(S_VALID.slice(-nPts))
  const point = intersect07(lngS) ?? [38.2, 1.57]
  const curve = []
  const step  = (point[0] - S22[0]) / 20
  for (let i = 0; i <= 20; i++) curve.push([S22[0] + i*step, lngS(S22[0] + i*step)])
  return { nPts, point, curve }
})

// Candidato activo: P3 (mejor según usuario)
const ACTIVE_N = 3
export const EAST_CAP_SOUTH = EAST_CAP_CANDIDATES.find(c => c.nPts === ACTIVE_N).point

// Sur corregido: S1…S22 + puntos de la curva P3 (la banda sigue la extrapolación P3)
const activeCandidate = EAST_CAP_CANDIDATES.find(c => c.nPts === ACTIVE_N)
const southCorrected = [...S_VALID, ...activeCandidate.curve]

// Curvas suaves Catmull-Rom
const NORTH_SMOOTH = catmullRom(clip64(NORTH_LIMIT))
const SOUTH_SMOOTH = catmullRom(southCorrected)

export const CENTERLINE_SMOOTH = catmullRom(clip64(CENTERLINE))
export { NORTH_SMOOTH, SOUTH_SMOOTH }

export const BAND_POLYGON = [
  ...clipCap(NORTH_SMOOTH),
  ...[...clipCap(SOUTH_SMOOTH)].reverse(),
]

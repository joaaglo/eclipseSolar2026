"""
add_centerline_dist.py — Añade columna Dist_centerline_km a eclipse_sitios_rutas.csv.

Calcula la distancia mínima de cada sitio a la línea central del eclipse
(polilínea de puntos NASA) usando Haversine punto-a-segmento.

Uso:
    python add_centerline_dist.py
Genera:
    eclipse_sitios_rutas.csv  (sobreescribe añadiendo la columna)
"""

import csv
import math

# Línea central NASA (lat, lng en grados decimales)
# Fuente: https://eclipse.gsfc.nasa.gov/SEpath/SEpath2001/SE2026Aug12Tpath.html
CENTERLINE = [
    (82.275, 112.487),
    (85.295, 104.215),
    (87.278, 81.525),
    (87.823, 33.000),
    (86.835, -1.638),
    (85.403, -15.182),
    (83.932, -21.187),
    (82.495, -24.272),
    (81.110, -25.992),
    (79.773, -26.982),
    (78.483, -27.540),
    (77.233, -27.825),
    (76.017, -27.928),
    (74.837, -27.905),
    (73.683, -27.788),
    (72.557, -27.603),
    (71.450, -27.362),
    (70.365, -27.078),
    (69.298, -26.760),
    (68.247, -26.410),
    (67.210, -26.032),
    (66.185, -25.630),
    (65.172, -25.205),
    (64.168, -24.757),
    (63.172, -24.287),
    (62.183, -23.793),
    (61.200, -23.277),
    (60.222, -22.737),
    (59.245, -22.170),
    (58.272, -21.573),
    (57.297, -20.947),
    (56.322, -20.287),
    (55.343, -19.588),
    (54.362, -18.847),
    (53.372, -18.057),
    (52.372, -17.212),
    (51.360, -16.303),
    (50.333, -15.317),
    (49.285, -14.238),
    (48.212, -13.048),
    (47.102, -11.715),
    (45.943, -10.190),
    (44.713, -8.398),
    (43.372, -6.188),
    (41.817, -3.185),
    (39.408, 2.950),
]

R = 6371.0  # radio Tierra en km

def to_rad(deg):
    return deg * math.pi / 180.0

def haversine(lat1, lng1, lat2, lng2):
    dlat = to_rad(lat2 - lat1)
    dlng = to_rad(lng2 - lng1)
    a = math.sin(dlat/2)**2 + math.cos(to_rad(lat1)) * math.cos(to_rad(lat2)) * math.sin(dlng/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def cross_track_distance(lat, lng, lat1, lng1, lat2, lng2):
    """Distancia de punto (lat,lng) al segmento (lat1,lng1)-(lat2,lng2).
    Usa cross-track distance esférica; si la proyección cae fuera del segmento,
    devuelve la distancia al extremo más cercano."""
    d13 = haversine(lat1, lng1, lat, lng) / R  # en radianes
    d12 = haversine(lat1, lng1, lat2, lng2) / R

    if d12 == 0:
        return haversine(lat1, lng1, lat, lng)

    # bearing lat1->lat (θ13) y lat1->lat2 (θ12)
    def bearing(la1, lo1, la2, lo2):
        la1, lo1, la2, lo2 = map(to_rad, [la1, lo1, la2, lo2])
        dlo = lo2 - lo1
        x = math.sin(dlo) * math.cos(la2)
        y = math.cos(la1) * math.sin(la2) - math.sin(la1) * math.cos(la2) * math.cos(dlo)
        return math.atan2(x, y)

    t13 = bearing(lat1, lng1, lat, lng)
    t12 = bearing(lat1, lng1, lat2, lng2)

    dxt = math.asin(math.sin(d13) * math.sin(t13 - t12))  # cross-track en radianes
    dat = math.acos(math.cos(d13) / math.cos(dxt))        # along-track en radianes

    # Si la proyección queda fuera del segmento, usar extremo más cercano
    if dat > d12 or math.cos(t13 - t12) < 0:
        return min(haversine(lat1, lng1, lat, lng), haversine(lat2, lng2, lat, lng))

    return abs(dxt) * R

def min_dist_to_centerline(lat, lng):
    dists = [
        cross_track_distance(lat, lng, CENTERLINE[i][0], CENTERLINE[i][1],
                             CENTERLINE[i+1][0], CENTERLINE[i+1][1])
        for i in range(len(CENTERLINE) - 1)
    ]
    return round(min(dists), 1)

def main():
    csv_path = "output/eclipse_sitios_rutas.csv"
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    from get_routes import SITES
    sites_by_name = {s[0]: (s[7], s[8]) for s in SITES}

    for row in rows:
        name = row["Espacio"]
        if name in sites_by_name:
            lat, lng = sites_by_name[name]
            row["Dist_centerline_km"] = min_dist_to_centerline(lat, lng)
        else:
            row["Dist_centerline_km"] = ""

    fieldnames = list(rows[0].keys())
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    print(f"Listo. Columna Dist_centerline_km añadida a {csv_path}")

    # Preview: los 10 sitios más cercanos a la línea central
    sorted_rows = sorted(
        [r for r in rows if r["Dist_centerline_km"] != ""],
        key=lambda r: float(r["Dist_centerline_km"])
    )
    print("\nTop 10 sitios más cercanos a la línea central:")
    print(f"{'Sitio':<45} {'Municipio':<30} {'Dist CL':>10}  {'Dur totalidad'}")
    print("-" * 100)
    for r in sorted_rows[:10]:
        print(f"{r['Espacio']:<45} {r['Municipio']:<30} {r['Dist_centerline_km']:>8} km  {r['Duración totalidad']}")

if __name__ == "__main__":
    main()

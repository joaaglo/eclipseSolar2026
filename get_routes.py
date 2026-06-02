"""
get_routes.py — Calcula distancias y tiempos por carretera desde Alboraya (46120)
usando OSRM (OpenStreetMap, sin API key).

Uso:
    python get_routes.py
Genera:
    eclipse_sitios_rutas.csv
"""

import csv
import time
import urllib.request
import urllib.error
import json

ORIGIN_LAT = 39.5516
ORIGIN_LNG = -0.3373
OSRM_URL = "http://router.project-osrm.org/route/v1/driving/{lng1},{lat1};{lng2},{lat2}?overview=false"

SITES = [
    ("MotorLand Aragón", "Alcañiz (Teruel)", "Circuito de carreras", "5.000", "Sí", "20:29:37", "1m 33s", 41.018, -0.322),
    ("Antiguo Aeródromo de Calamocha", "Calamocha (Teruel)", "Lugar de interés histórico", "5.000", "Sí", "20:30:04", "1m 42s", 40.904, -1.295),
    ("Estación de Esquí Javalambre", "Camarena de la Sierra (Teruel)", "Estación de esquí", "5.000", "Sí", "20:31:19", "1m 28s", 40.060, -1.012),
    ("Monreal del Campo", "Monreal del Campo (Teruel)", "(sin especificar)", "5.000", "Sí", "20:30:17", "1m 41s", 40.789, -1.357),
    ("Ariza", "Ariza (Zaragoza)", "(sin especificar)", "5.000", "Sí", "20:29:38", "1m 42s", 41.329, -2.039),
    ("Polígono de Cariñena", "Cariñena (Zaragoza)", "Polígono industrial", "5.000", "Sí", "20:29:25", "1m 38s", 41.340, -1.225),
    ("Polígono de Épila", "Épila (Zaragoza)", "Polígono industrial", "5.000", "Sí", "20:29:04", "1m 32s", 41.606, -1.277),
    ("Acantilado del Cabo de Peñas", "Gozón (Asturias)", "Espacio natural", "-", "-", "20:26:36", "1m 44s", 43.663, -5.849),
    ("Playa de Verdicio", "Gozón (Asturias)", "Playa", "-", "-", "20:26:36", "1m 44s", 43.630, -5.916),
    ("Playa de Xagó", "Gozón (Asturias)", "Playa", "-", "-", "20:26:36", "1m 44s", 43.618, -5.945),
    ("Semáforo del Cabo de Peñas", "Gozón (Asturias)", "Espacio natural", "-", "-", "20:26:36", "1m 44s", 43.663, -5.849),
    ("Cabo de Busto", "Luarca-Valdés (Asturias)", "Espacio natural", "4.000", "Sí", "20:26:47", "1m 49s", 43.583, -6.472),
    ("Gamones", "Luarca-Valdés (Asturias)", "Explanada", "4.000", "Sí", "20:26:47", "1m 49s", 43.540, -6.530),
    ("De Campa Torres a Playa de Poniente", "Gijón (Asturias)", "Paseo marítimo", "-", "-", "20:26:42", "1m 45s", 43.562, -5.680),
    ("De Puente del Piles a Parque de la Providencia", "Gijón (Asturias)", "Paseo marítimo", "-", "-", "20:26:42", "1m 45s", 43.540, -5.660),
    ("Barrio del Carrasqueo", "Luarca-Valdés (Asturias)", "Carretera", "800", "Sí", "20:26:47", "1m 49s", 43.543, -6.527),
    ("Barrio del Mirador", "Luarca-Valdés (Asturias)", "Calle", "400", "Sí", "20:26:47", "1m 49s", 43.543, -6.527),
    ("Bosque-Jardín de la Fonte Baxa", "Luarca-Valdés (Asturias)", "Espacio natural", "1.000", "Sí", "20:26:47", "1m 49s", 43.543, -6.527),
    ("Carretera del Faro", "Luarca-Valdés (Asturias)", "Carretera", "1.000", "Sí", "20:26:47", "1m 49s", 43.543, -6.527),
    ("Mirador de la Funiar", "Luarca-Valdés (Asturias)", "Mirador", "600", "Sí", "20:26:47", "1m 49s", 43.543, -6.527),
    ("Paseo del Muelle", "Luarca-Valdés (Asturias)", "Paseo marítimo", "-", "Sí", "20:26:47", "1m 49s", 43.543, -6.527),
    ("Villar", "Luarca-Valdés (Asturias)", "Explanada", "5.000", "Sí", "20:26:47", "1m 49s", 43.543, -6.527),
    ("Faro de Ajo", "Bareyo (Cantabria)", "Espacio natural", "-", "-", "20:26:54", "51s", 43.508, -3.584),
    ("Peña Cabarga", "Medio Cudeyo (Cantabria)", "Espacio natural", "-", "-", "20:26:57", "1m 07s", 43.421, -3.740),
    ("Observatorio Astronómico de Cantabria", "Páramo de la Lora (Cantabria)", "Espacio natural", "-", "-", "20:27:40", "1m 38s", 42.863, -3.920),
    ("la Virgen del Mar", "Santander (Cantabria)", "Espacio natural", "-", "-", "20:26:52", "1m 03s", 43.490, -3.810),
    ("Suances", "Suences (Cantabria)", "(sin especificar)", "-", "-", "20:26:52", "1m 15s", 43.437, -4.047),
    ("Evento Eclipsados Ávila", "Arévalo (Ávila)", "Explanada", "-", "-", "20:31:10", "37s", 41.063, -4.721),
    ("Embalse del Ebro", "Arija (Burgos)", "Playa", "3.000-5.000", "Sí", "20:27:25", "1m 32s", 42.958, -3.952),
    ("Mirador de San Cibrián", "Hacinas (Burgos)", "Parque", "2", "Sí", "20:28:49", "1m 44s", 41.951, -3.246),
    ("Centro Astronómico de Lodoso", "Lodoso (Burgos)", "Centro astronómico", "2", "Sí", "20:28:15", "1m 44s", 42.340, -3.780),
    ("Parque eólico páramo de Poza", "Poza de la Sal (Burgos)", "Parque eólico", "5", "Sí", "20:27:50", "1m 35s", 42.672, -3.513),
    ("Cerro afueras de Quintanarraya", "Quintanarraya (Burgos)", "Espacio natural", "1", "Sí", "20:29:04", "1m 45s", 41.840, -3.191),
    ("Zona de barbacoas", "Santo Domingo de Silos (Burgos)", "Espacio natural", "-", "-", "20:28:53", "1m 44s", 41.963, -3.415),
    ("Afueras de Tejada", "Tejada (Burgos)", "Espacio natural", "500", "Sí", "20:28:55", "1m 45s", 41.970, -3.360),
    ("La Camperona", "Sabero (León)", "Montaña", "-", "-", "20:27:46", "1m 47s", 42.835, -5.096),
    ("Palacio de Congresos y Exposiciones", "León (León)", "Explanada", "-", "-", "20:28:15", "1m 45s", 42.598, -5.571),
    ("Mirador de los Caballos Thieldones", "Saldaña (Palencia)", "Mirador", "-", "-", "20:28:13", "1m 47s", 42.517, -4.743),
    ("Arcones", "Arcones (Segovia)", "(sin especificar)", "-", "-", "20:30:28", "1m 25s", 41.124, -3.681),
    ("Ayllón", "Ayllón (Segovia)", "(sin especificar)", "-", "-", "20:29:47", "1m 40s", 41.426, -3.369),
    ("Boceguillas", "Boceguillas (Segovia)", "(sin especificar)", "-", "-", "20:30:01", "1m 35s", 41.329, -3.641),
    ("Collado Hermoso", "Collado Hermoso (Segovia)", "(sin especificar)", "-", "-", "20:30:44", "1m 14s", 41.011, -3.800),
    ("Otero de Herreros", "Otero de Herreros (Segovia)", "(sin especificar)", "-", "-", "20:31:27", "36s", 40.721, -4.099),
    ("Riaza", "Riaza (Segovia)", "(sin especificar)", "-", "-", "20:30:04", "1m 35s", 41.277, -3.487),
    ("Segovia", "Segovia (Segovia)", "(sin especificar)", "-", "-", "20:31:03", "58s", 40.948, -4.118),
    ("Turégano", "Turégano (Segovia)", "(sin especificar)", "-", "-", "20:30:31", "1m 19s", 41.148, -4.016),
    ("Alto del Moncayo (Cima de Peña Negrilla)", "Ágreda (Soria)", "Montaña", "-", "-", "20:28:48", "1m 34s", 41.799, -1.839),
    ("Sierra de Aleza", "Buberos (Soria)", "Montaña", "-", "-", "20:29:09", "1m 41s", 41.615, -2.208),
    ("Muralla de Almazán", "Almazán (Soria)", "Monumento", "-", "-", "20:29:27", "1m 44s", 41.488, -2.524),
    ("Cerro de Borobia", "Borobia (Soria)", "Espacio natural", "-", "-", "20:29:04", "1m 38s", 41.754, -1.930),
    ("Castillo de Cabrejas del Pinar", "Cabrejas del Pinar (Soria)", "Monumento", "-", "-", "20:29:02", "1m 44s", 41.735, -2.769),
    ("Castillo de Calatañazor", "Calatañazor (Soria)", "Monumento", "-", "-", "20:29:11", "1m 44s", 41.697, -2.819),
    ("Pico de Urbión", "Duruelo de la Sierra (Soria)", "Montaña", "-", "-", "20:28:48", "1m 43s", 41.998, -2.888),
    ("Campamento de Alto Real", "Garray (Soria)", "Explanada", "-", "-", "20:28:56", "1m 41s", 41.829, -2.397),
    ("Numancia", "Garray (Soria)", "Auditorio al aire libre", "3.000", "-", "20:28:56", "1m 41s", 41.808, -2.435),
    ("Fortaleza de Gormaz", "Gormaz (Soria)", "Monumento", "-", "-", "20:29:33", "1m 44s", 41.480, -3.017),
    ("Castillo de Medinaceli", "Medinaceli (Soria)", "Explanada", "-", "-", "20:29:57", "1m 42s", 41.172, -2.431),
    ("Tiermes", "Montejo de Tiermes (Soria)", "Yacimiento arqueológico", "-", "-", "20:29:50", "1m 40s", 41.350, -3.171),
    ("Augustóbriga", "Ólvega (Soria)", "Yacimiento arqueológico", "-", "-", "20:28:55", "1m 37s", 41.783, -1.989),
    ("Uxama", "El Burgo de Osma-Ciudad de Osma (Soria)", "Yacimiento arqueológico", "-", "-", "20:29:25", "1m 44s", 41.560, -3.060),
    ("Muela de Peñalcázar", "Quiñonería (Soria)", "Espacio natural", "-", "-", "20:29:14", "1m 41s", 41.549, -2.337),
    ("Sierra de Perdices", "Viana de Duero (Soria)", "Espacio natural", "-", "-", "20:29:22", "1m 44s", 41.510, -2.870),
    ("Eras de Rioseco", "Rioseco de Soria (Soria)", "Explanada", "-", "-", "20:29:17", "1m 44s", 41.682, -2.564),
    ("Cerro de San Leonardo de Yagüe", "San Leonardo de Yagüe (Soria)", "Espacio natural", "-", "-", "20:29:01", "1m 45s", 41.829, -2.981),
    ("Monte Valonsadero", "Soria (Soria)", "Espacio natural", "30.000", "-", "20:29:01", "1m 41s", 41.800, -2.434),
    ("Mirador de la Galiana", "Ucero (Soria)", "Espacio natural", "-", "-", "20:29:12", "1m 44s", 41.652, -2.969),
    ("Alcazaren", "Alcazaren (Valladolid)", "(sin especificar)", "-", "-", "20:30:20", "1m 14s", 41.383, -4.710),
    ("Becilla de Valderaduey", "Becilla de Valderaduey (Valladolid)", "Espacio natural", "-", "-", "20:29:05", "1m 36s", 42.001, -5.174),
    ("Cabezón del Pisuerga", "Cabezón del Pisuerga (Valladolid)", "(sin especificar)", "-", "-", "20:29:36", "1m 33s", 41.727, -4.623),
    ("Campaspero", "Campaspero (Valladolid)", "(sin especificar)", "-", "-", "20:29:55", "1m 31s", 41.374, -4.176),
    ("Castrodeza", "Castrodeza (Valladolid)", "(sin especificar)", "-", "-", "20:29:53", "1m 22s", 41.540, -4.887),
    ("Cigales", "Cigales (Valladolid)", "(sin especificar)", "-", "-", "20:29:34", "1m 33s", 41.763, -4.682),
    ("Encinas de Esgueva", "Encinas de Esgueva (Valladolid)", "(sin especificar)", "-", "-", "20:29:23", "1m 41s", 41.706, -3.948),
    ("Íscar", "Íscar (Valladolid)", "(sin especificar)", "-", "-", "20:30:18", "1m 17s", 41.367, -4.542),
    ("La Cisterniga", "La Cisterniga (Valladolid)", "(sin especificar)", "-", "-", "20:29:51", "1m 27s", 41.631, -4.669),
    ("La Parrilla", "La Parrilla (Valladolid)", "(sin especificar)", "-", "-", "20:29:57", "1m 27s", 41.526, -4.496),
    ("Medina de Rioseco", "Medina de Rioseco (Valladolid)", "(sin especificar)", "-", "-", "20:29:27", "1m 31s", 41.879, -5.042),
    ("Piñel de Abajo", "Piñel de Abajo (Valladolid)", "(sin especificar)", "-", "-", "20:29:33", "1m 38s", 41.655, -3.997),
    ("Portillo", "Portillo (Valladolid)", "(sin especificar)", "-", "-", "20:30:05", "1m 22s", 41.488, -4.539),
    ("Rueda", "Rueda (Valladolid)", "(sin especificar)", "-", "-", "20:30:24", "1m 06s", 41.401, -4.965),
    ("San Miguel de Pino", "San Miguel de Pino (Valladolid)", "(sin especificar)", "-", "-", "20:29:47", "1m 28s", 41.522, -5.009),
    ("San Miguel del Arroyo", "San Miguel del Arroyo (Valladolid)", "(sin especificar)", "-", "-", "20:30:06", "1m 24s", 41.437, -4.362),
    ("Tiedra", "Tiedra (Valladolid)", "(sin especificar)", "-", "-", "20:30:01", "1m 13s", 41.753, -5.210),
    ("Trigueros del Valle", "Trigueros del Valle (Valladolid)", "(sin especificar)", "-", "-", "20:29:25", "1m 36s", 41.840, -4.451),
    ("Tudela de Duero", "Tudela de Duero (Valladolid)", "(sin especificar)", "-", "-", "20:29:52", "1m 28s", 41.586, -4.575),
    ("Urones de Castroponce", "Urones de Castroponce (Valladolid)", "(sin especificar)", "-", "-", "20:29:06", "1m 35s", 42.012, -5.291),
    ("Urueña", "Urueña (Valladolid)", "(sin especificar)", "-", "-", "20:29:49", "1m 20s", 41.803, -5.168),
    ("Villalón de Campos", "Villalón de Campos (Valladolid)", "(sin especificar)", "-", "-", "20:29:01", "1m 40s", 42.059, -4.996),
    ("Villanueva de Duero", "Villanueva de Duero (Valladolid)", "(sin especificar)", "-", "-", "20:30:08", "1m 16s", 41.510, -4.780),
    ("Avenida Cardenal Cisneros", "Zamora (Zamora)", "Explanada", "-", "-", "20:30:48", "19s", 41.504, -5.745),
    ("Avenida de la Frontera", "Zamora (Zamora)", "Espacio natural", "-", "-", "20:30:48", "19s", 41.504, -5.745),
    ("Camino de Valbueno", "Zamora (Zamora)", "Espacio natural", "-", "-", "20:30:48", "19s", 41.504, -5.745),
    ("Castillo de Zamora", "Zamora (Zamora)", "Castillo", "-", "-", "20:30:48", "19s", 41.504, -5.745),
    ("Mirador de La Lobata", "Zamora (Zamora)", "Mirador", "-", "-", "20:30:48", "19s", 41.504, -5.745),
    ("Parada del Molino", "Zamora (Zamora)", "Parque", "-", "-", "20:30:48", "19s", 41.504, -5.745),
    ("Parque del Castillo", "Zamora (Zamora)", "Parque", "-", "-", "20:30:48", "19s", 41.504, -5.745),
    ("Paseo de las Vistillas", "Zamora (Zamora)", "Parque", "-", "-", "20:30:48", "19s", 41.504, -5.745),
    ("Cerro afueras de Cañete", "Cañete (Cuenca)", "Zona rural", "3.000", "Sí", "20:31:48", "1m 10s", 39.883, -1.657),
    ("Aparcamiento de la Fuensanta", "Cuenca (Cuenca)", "Explanada", "-", "Sí", "20:31:59", "56s", 40.065, -2.135),
    ("Museo Paleontológico de Castilla-La Mancha", "Cuenca (Cuenca)", "Explanada", "", "Sí", "20:31:59", "56s", 40.065, -2.135),
    ("Vertiente de Hoya Román", "Cuenca (Cuenca)", "Zona rural", "-", "Sí", "20:31:59", "56s", 40.065, -2.135),
    ("Cancha el Frontón", "Cuevas de Velasco (Cuenca)", "Cancha de Fútbol", "500", "Sí", "20:31:59", "51s", 40.170, -2.390),
    ("Castillo de Huete", "Huete (Cuenca)", "Castillo", "1.000", "Sí", "20:32:13", "32s", 40.145, -2.693),
    ("Palacio de los Condes de Priego", "Priego (Cuenca)", "Plaza", "2.000", "Sí", "20:31:15", "1m 19s", 40.438, -2.312),
    ("Plaza de toros Rodena", "Talayuelas (Cuenca)", "Plaza de toros", "1.500", "Sí", "20:32:02", "1m 06s", 39.876, -1.254),
    ("Paraje Solana la Virgen", "Tragacete (Cuenca)", "Zona rural", "2.500", "Sí", "20:31:15", "1m 24s", 40.350, -1.851),
    ("Plaza de toros de Villalba del Rey", "Villalba del Rey (Cuenca)", "Plaza de toros", "800", "Sí", "20:31:39", "1m 01s", 40.231, -2.615),
    ("Recinto Ferial de Azuqueca", "Azuqueca de Henares (Guadalajara)", "Campo de feria", "5.000", "500", "20:31:28", "58s", 40.563, -3.266),
    ("Campo de fútbol de Cabanillas", "Cabanillas del Campo (Guadalajara)", "Explanada", "60", "30", "20:31:17", "1m 06s", 40.627, -3.224),
    ("Mirador del castillo", "Chiloeches (Guadalajara)", "Mirador", "50", "20", "20:31:24", "1m 03s", 40.529, -3.235),
    ("Castillo de Cifuentes", "Cifuentes (Guadalajara)", "Mirador", "1.000", "Sí", "20:30:42", "1m 30s", 40.779, -2.616),
    ("Observatorio de Cogolludo", "Cogolludo (Guadalajara)", "Mirador", "1.000", "300", "20:30:34", "1m 29s", 40.954, -3.085),
    ("El Calvario de El Casar", "El Casar (Guadalajara)", "Mirador", "1.000", "250", "20:31:15", "1m 04s", 40.694, -3.338),
    ("Guadalajara", "Guadalajara (Guadalajara)", "(sin especificar)", "-", "-", "20:31:15", "1m 08s", 40.634, -3.165),
    ("Acceso al cementerio de Hita", "Hita (Guadalajara)", "Zona rural", "2.000", "1.000", "20:30:48", "1m 23s", 40.834, -3.052),
    ("Parque de Ferias de Marchamalo", "Marchamalo (Guadalajara)", "Campo de feria", "1.500", "300", "20:31:12", "1m 09s", 40.663, -3.206),
    ("Punto Limpio de Molina de Aragón", "Molina de Aragón (Guadalajara)", "Zona rural", "3.000", "Sí", "20:30:21", "1m 40s", 40.846, -1.886),
    ("Piscina municipal de Tamajón", "Tamajón (Guadalajara)", "Espacio natural con piscina", "200", "50", "20:30:31", "1m 29s", 40.960, -3.319),
    ("Campo de fútbol de Tórtola de Henares", "Tórtola de Henares (Guadalajara)", "Polideportivo", "50", "Sí", "20:31:05", "1m 14s", 40.585, -3.118),
    ("Club Motocross Yunquera", "Yunquera de Henares (Guadalajara)", "Circuito de carreras", "-", "-", "20:31:00", "1m 16s", 40.691, -3.188),
    ("Zona esportiva", "Les Borges Blanques (Lleida)", "Campo de fútbol", "2.650", "1.070", "20:29:11", "24s", 41.506, 0.869),
    ("Els Magraners", "Lleida (Lleida)", "Explanada", "4.300", "1.950", "20:29:05", "27s", 41.620, 0.607),
    ("Gardeny", "Lleida (Lleida)", "Explanada", "1.500", "600", "20:29:05", "27s", 41.610, 0.600),
    ("Secà de Sant Pere", "Lleida (Lleida)", "Explanada", "1.400", "980", "20:29:05", "27s", 41.618, 0.605),
    ("Plaça de bous de Alcanar", "Alcanar (Tarragona)", "Plaza de toros", "-", "-", "20:30:12", "1m 37s", 40.538, 0.479),
    ("Font del mirador d'Altafulla", "Altafulla (Tarragona)", "Explanada", "430", "180", "20:29:23", "52s", 41.140, 1.379),
    ("Polígon Industrial l'Oriola", "Amposta (Tarragona)", "Explanada", "4.400", "3.300", "20:29:56", "1m 34s", 40.705, 0.585),
    ("Camarles", "Camarles (Tarragona)", "(sin especificar)", "-", "-", "20:29:50", "1m 31s", 40.742, 0.639),
    ("Cooperativa Agrícola de Cambrils", "Cambrils (Tarragona)", "Explanada", "-", "-", "20:29:27", "1m 09s", 41.069, 1.060),
    ("Carrer Joan Miró", "Constantí (Tarragona)", "Explanada", "1.600", "680", "20:29:22", "58s", 41.155, 1.237),
    ("Polígon Industrial la Plana", "Gandesa (Tarragona)", "Explanada", "2.000", "1.800", "20:29:32", "1m 24s", 41.059, 0.446),
    ("Can Gironès", "L'Aldea (Tarragona)", "Explanada", "4.500", "2.500", "20:29:54", "1m 32s", 40.737, 0.615),
    ("Camp de futbol", "L'Atmetlla de Mar (Tarragona)", "Campo de fútbol", "1.250", "500", "20:29:41", "1m 25s", 40.878, 0.835),
    ("les Palomeres", "Montbrió del Camp (Tarragona)", "Explanada", "2.500", "600", "20:29:24", "1m 07s", 41.075, 1.095),
    ("Fira de Móra la Nova", "Móra la Nova (Tarragona)", "Campo de feria", "3.800", "1.500", "20:29:27", "1m 18s", 41.094, 0.642),
    ("Horts del Queri", "Reus (Tarragona)", "Parque", "1.750", "900", "20:29:22", "1m 01s", 41.149, 1.097),
    ("Parc de la Festa de Reus", "Reus (Tarragona)", "Explanada", "5.000", "2.500", "20:29:22", "1m 01s", 41.155, 1.107),
    ("Carretera de la Galera", "Santa Bárbara (Tarragona)", "Explanada", "1.100", "520", "20:29:57", "1m 34s", 40.598, 0.453),
    ("L'Anella Mediterrànea", "Tarragona (Tarragona)", "Parque", "-", "-", "20:29:24", "59s", 41.121, 1.249),
    ("La Marina Tárraco", "Tarragona (Tarragona)", "Puerto deportivo", "-", "-", "20:29:24", "59s", 41.119, 1.248),
    ("Polígon Industrial de Roques Planes", "Torredembarra (Tarragona)", "Explanada", "1.170", "570", "20:29:23", "51s", 41.145, 1.396),
    ("Polígon Industrial de Valls", "Valls (Tarragona)", "Explanada", "4.100", "1.900", "20:29:18", "41s", 41.282, 1.249),
    ("Ermita de San Cristóbal", "Benasal (Castellón)", "Espacio natural", "1.000", "Sí", "20:30:37", "1m 39s", 40.371, -0.164),
    ("Playas del Pinar y del Gurugú", "Castellón de la Plana (Castellón)", "Playa", "50.000", "Sí", "20:31:14", "1m 33s", 39.990, -0.010),
    ("Parque municipal de Les Useres", "Les Useres (Castellón)", "Parque", "2.000", "Sí", "20:30:59", "1m 37s", 40.157, -0.186),
    ("Peñíscola", "Peñíscola (Castellón)", "(sin especificar)", "5.000", "Sí", "20:30:37", "1m 39s", 40.360, 0.401),
    ("Partidas, en Aras de los Olmos", "Aras de los Olmos (Valencia)", "Espacio natural", "5.000", "Sí", "20:31:48", "1m 15s", 39.920, -1.116),
    ("Muela de Santa Catalina", "Aras de los Olmos (Valencia)", "Espacio natural", "1.000", "Sí", "20:31:48", "1m 15s", 39.920, -1.116),
    ("Castillo de Macastre", "Macastre (Valencia)", "Espacio natural", "4.500", "Sí", "20:32:58", "23s", 39.370, -0.760),
    ("Playa de Puzol", "Puzol (Valencia)", "Playa", "1.000", "Sí", "20:32:03", "1m 13s", 39.627, -0.266),
    ("Pico del Remedio", "Utiel (Valencia)", "Espacio natural", "2.000", "Sí", "20:32:43", "33s", 39.567, -1.207),
    ("Playa de la Malvarrosa", "Valencia (Valencia)", "Playa", "10.000", "Sí", "20:32:24", "1m", 39.477, -0.335),
    ("Estaca de Bares", "Mañón (A Coruña)", "Espacio natural", "-", "-", "20:26:38", "1m 47s", 43.785, -7.685),
    ("Garita de Bares", "Mañón (A Coruña)", "Mirador", "-", "-", "20:26:38", "1m 47s", 43.785, -7.685),
    ("Semáforo de Bares", "Mañón (A Coruña)", "Mirador", "-", "-", "20:26:38", "1m 47s", 43.785, -7.685),
    ("Castillo de San Antón", "A Coruña (A Coruña)", "Paseo marítimo", "-", "-", "20:27:35", "1m 16s", 43.369, -8.390),
    ("Paseo Marítimo central", "A Coruña (A Coruña)", "Paseo marítimo", "-", "-", "20:27:35", "1m 16s", 43.369, -8.390),
    ("Paseo Marítimo O Portiño", "A Coruña (A Coruña)", "Paseo marítimo", "-", "-", "20:27:35", "1m 16s", 43.369, -8.390),
    ("Playa de Riazor-Orzán", "A Coruña (A Coruña)", "Playa", "-", "-", "20:27:35", "1m 16s", 43.369, -8.390),
    ("Alcalá de Henares", "Alcalá de Henares (Madrid)", "(sin especificar)", "-", "-", "20:31:47", "40s", 40.482, -3.364),
    ("Las piscinas de Riosequillo", "Buitrago del Lozoya (Madrid)", "Espacio natural", "-", "-", "20:30:42", "1m 19s", 41.004, -3.617),
    ("Puerto de Navacerrada", "Cercedilla (Madrid)", "(sin especificar)", "-", "-", "20:31:34", "35s", 40.783, -4.010),
    ("Colmenar Viejo", "Colmenar Viejo (Madrid)", "(sin especificar)", "-", "-", "20:31:35", "41s", 40.659, -3.769),
    ("El Molar", "El Molar (Madrid)", "(sin especificar)", "-", "-", "20:31:15", "1m 01s", 40.734, -3.578),
    ("La Cabrera", "La Cabrera (Madrid)", "(sin especificar)", "-", "-", "20:30:58", "1m 11s", 40.858, -3.624),
    ("Meco", "Meco (Madrid)", "(sin especificar)", "-", "-", "20:31:33", "52s", 40.558, -3.337),
    ("San Agustín del Guadalix", "San Agustín del Guadalix (Madrid)", "(sin especificar)", "-", "-", "20:31:25", "53s", 40.697, -3.615),
    ("Campo de fútbol Calle Teide", "San Sebastián de los Reyes (Madrid)", "Explanada", "20.000", "-", "20:31:48", "31s", 40.550, -3.627),
    ("Villa de Somosierra", "Somosierra (Madrid)", "(sin especificar)", "-", "-", "20:30:23", "1m 29s", 41.155, -3.577),
    ("Tres Cantos", "Tres Cantos (Madrid)", "(sin especificar)", "-", "-", "20:31:42", "36s", 40.600, -3.700),
    ("Sendaviva", "Arguedas (Navarra)", "Parque de atracciones", "-", "-", "20:28:23", "1m 13s", 42.107, -1.600),
    ("Bardenas Reales - Embalse El Ferial", "Mélida (Navarra)", "Espacio natural", "-", "-", "20:28:13", "57s", 42.173, -1.530),
    ("Bardenas Reales - Aguilares", "Arguedas (Navarra)", "Centro de visitantes", "-", "-", "20:28:23", "1m 13s", 42.107, -1.600),
    ("Arguedas", "Arguedas (Navarra)", "(sin especificar)", "-", "-", "20:28:23", "1m 13s", 42.107, -1.600),
    ("Buñuel", "Buñuel (Navarra)", "(sin especificar)", "-", "-", "20:28:36", "1m 20s", 41.976, -1.762),
    ("Cárcar", "Cárcar (Navarra)", "(sin especificar)", "-", "-", "20:28:09", "1m 11s", 42.364, -1.927),
    ("Cascante", "Cascante (Navarra)", "(sin especificar)", "-", "-", "20:28:35", "1m 25s", 42.001, -1.681),
    ("Castejón", "Castejón (Navarra)", "(sin especificar)", "-", "-", "20:28:24", "1m 16s", 42.162, -1.694),
    ("Corella", "Corella (Navarra)", "(sin especificar)", "-", "-", "20:28:27", "1m 22s", 42.115, -1.786),
    ("Fitero", "Fitero (Navarra)", "(sin especificar)", "-", "-", "20:28:32", "1m 26s", 42.060, -1.866),
    ("Larraga", "Larraga (Navarra)", "(sin especificar)", "-", "-", "20:28:01", "52s", 42.564, -1.848),
    ("Campo de Fútbol Viejo de Lerín", "Lerín (Navarra)", "Explanada", "5.000", "Sí", "20:28:04", "1m 04s", 42.476, -2.004),
    ("Lodosa", "Lodosa (Navarra)", "(sin especificar)", "-", "-", "20:28:07", "1m 12s", 42.420, -2.070),
    ("Marcilla", "Marcilla (Navarra)", "(sin especificar)", "-", "-", "20:28:14", "1m 07s", 42.312, -1.716),
    ("Mendavia", "Mendavia (Navarra)", "(sin especificar)", "-", "-", "20:28:05", "1m 15s", 42.445, -2.181),
    ("Peralta", "Peralta (Navarra)", "(sin especificar)", "-", "-", "20:28:13", "1m 08s", 42.337, -1.806),
    ("Ribaforada", "Ribaforada (Navarra)", "(sin especificar)", "-", "-", "20:28:35", "1m 21s", 41.996, -1.641),
    ("Tafalla", "Tafalla (Navarra)", "(sin especificar)", "-", "-", "20:28:05", "45s", 42.529, -1.674),
    ("Tudela", "Tudela (Navarra)", "(sin especificar)", "-", "-", "20:28:31", "1m 20s", 42.062, -1.608),
    ("Viana", "Viana (Navarra)", "(sin especificar)", "-", "-", "20:28:00", "1m 16s", 42.513, -2.374),
]

def get_route(dest_lat, dest_lng):
    url = OSRM_URL.format(
        lng1=ORIGIN_LNG, lat1=ORIGIN_LAT,
        lng2=dest_lng, lat2=dest_lat
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "eclipse-planner/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        route = data["routes"][0]
        dist_km = round(route["distance"] / 1000, 1)
        dur_min = round(route["duration"] / 60)
        h, m = divmod(dur_min, 60)
        dur_str = f"{h}h {m:02d}min" if h else f"{m}min"
        return dist_km, dur_str
    except Exception as e:
        return None, f"ERROR: {e}"

def main():
    out = []
    total = len(SITES)
    for i, s in enumerate(SITES):
        name, loc, tipo, cap, park, inicio, dur, lat, lng = s
        print(f"[{i+1}/{total}] {name}...", end=" ", flush=True)
        dist_km, dur_str = get_route(lat, lng)
        print(f"{dist_km} km, {dur_str}")
        out.append({
            "Espacio": name,
            "Municipio": loc,
            "Tipo": tipo,
            "Capacidad": cap,
            "Parking": park,
            "Inicio totalidad": inicio,
            "Duración totalidad": dur,
            "Dist_carretera_km": dist_km if dist_km else "",
            "Tiempo_Maps": dur_str,
        })
        time.sleep(0.3)  # ser amables con OSRM

    with open("eclipse_sitios_rutas.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)

    print(f"\nListo. Guardado en eclipse_sitios_rutas.csv")

if __name__ == "__main__":
    main()

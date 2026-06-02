import json, sys
sys.path.insert(0, '.')
from get_routes import SITES
keys = ['espacio','municipio','tipo','capacidad','parking','inicio_totalidad','duracion_totalidad','lat','lng']
data = [dict(zip(keys, s)) for s in SITES]
with open('sites.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f'OK: {len(data)} sitios -> sites.json')

import requests
import csv
import json

# URL del servicio REST de Esri
service_url = "https://serviciosgis.catastrobogota.gov.co/arcgis/rest/services/catastro/valorreferencia/MapServer/12/query"

# Ruta al archivo CSV que contiene los códigos de manzanas
csv_file_path = r"C:\Users\Juan Dallos\Desktop\NNAavaluo\manzanas.csv"  # Usar 'r' para rutas sin escape

# Campos a solicitar
out_fields = "MANCODIGO,V_REF"

# Función para hacer solicitudes al servicio y obtener los datos
def get_data_from_service(codes):
    where_clause = "MANCODIGO IN ('{}')".format("','".join(codes))  # Agregar comillas a cada código
    params = {
        "where": where_clause,
        "outFields": "*",
        "f": "json"
    }
    response = requests.get(service_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error en la solicitud:", response.status_code)
        return None

# Cargar los códigos de manzanas desde el archivo CSV
codes_list = []
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Saltar la fila de encabezados si es necesario
    for row in csv_reader:
        if row:  # Asegurarse de que la fila no esté vacía
            codes_list.append(row[0])  # Supongamos que el código está en la primera columna

# Dividir los códigos en grupos de 1000 para realizar las solicitudes
group_size = 20
for i in range(0, len(codes_list), group_size):
    group = codes_list[i:i+group_size]
    data = get_data_from_service(group)
    if data:
        # Crear un GeoJSON a partir de los datos completos obtenidos
        geojson = {
            "type": "FeatureCollection",
            "features": []
        }
        
        for feature in data['features']:
            geojson_feature = {
                "type": "Feature",
                "properties": feature['attributes'],
                "geometry": feature['geometry']
            }
            geojson['features'].append(geojson_feature)
        
        # Guardar el GeoJSON en un archivo
        with open(f'data_group_{i}.geojson', 'w') as geojson_file:
            json.dump(geojson, geojson_file, indent=2)
    else:
        print("No se pudieron obtener datos para el grupo:", group)